#include <string.h>
#include <memory.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include "cmac.h"
#include "aes.h"
#include "challenge.h"
#include "claa_base.h"
/* 十六进制数转换为十进制数 */
long hexToDec(char *source);

/* 返回ch字符在sign数组中的序号 */
int getIndexOfSigns(char ch);


long hexToDec(char *source)
{
    long sum = 0;
    long t = 1;
    int i, len;

    len = strlen(source);
    for(i=len-1; i>=0; i--)
    {
        sum += t * getIndexOfSigns(*(source + i));
        t *= 16;
    }

    return sum;
}

/* 返回ch字符在sign数组中的序号 */
int getIndexOfSigns(char ch)
{
    if(ch >= '0' && ch <= '9')
    {
        return ch - '0';
    }
    if(ch >= 'A' && ch <='F')
    {
        return ch - 'A' + 10;
    }
    if(ch >= 'a' && ch <= 'f')
    {
        return ch - 'a' + 10;
    }
    return -1;
}

/*
// C prototype : void str2hex(uint8*pbDest, uint8*pbSrc, int nLen)
// parameter(s): [OUT] pbDest - 输出缓冲区
// [IN] pbSrc - 字符串
// [IN] nLen - 16进制数的字节数(字符串的长度/2)
// return value: 
// remarks : 将字符串转化为16进制数
*/
void str2hex(uint8*pbDest, uint8*pbSrc, int nLen)
{
        char h1,h2;
        uint8 s1,s2;
        int i;

        for (i=0; i<nLen; i++)
        {
                h1 = pbSrc[2*i];
                h2 = pbSrc[2*i+1];

                s1 = toupper(h1) - 0x30;
                if (s1 > 9)
                        s1 -= 7;

                s2 = toupper(h2) - 0x30;
                if (s2 > 9)
                        s2 -= 7;

                pbDest[i] = s1*16 + s2;
        }
}
/*
int main(int argc,char*argv[])
{
        uint8 appkey[APPKEY_LEN];//={0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff};
        uint8*psrc = "00112233445566778899aabbccddeeff";
        str2hex(appkey,psrc,16);

        char *appeui = "2c26c50065650041";
        uint32 appnonce = 2112283883;


        char chall[32+1];

        //challenge_identification(appkey,3181446792275624001,appnonce,chall);
        challenge_identification(appkey,hexToDec(appeui),appnonce,chall);

        printf("chall=%s\n",chall);


        return 0;
}
*/
void get_challenge(char *appkey,char *appeui,uint32 appnonce, char *challenge)
{
	uint8 _appkey[APPKEY_LEN];
	str2hex(_appkey,appkey,16);

	challenge_identification(_appkey,hexToDec(appeui),appnonce,challenge);
}
void challenge_identification(uint8 appkey[APPKEY_LEN], uint64 appeui, uint32 appnonce, char*challenge)
{
	uint8 *ptmp = NULL;
	uint8 msg[16] = { 0 };
	uint8 tmp_challenge[16] = { 0 };
	//schar challenge[32 + 1] = { '\0' };
	AES_CMAC_CTX cmacctx;
	uint8 i, j;
	uint8 high, low;
	uint8 flag = 0;

	/*
	* 生成msg
	* msg = appeui|appnonce|0 (注：msg最后补32位的0，成128bit信息块)
	*/
	ptmp = (uint8 *)(&appeui);
	for (i = 0; i<8; i++)
	{
		msg[i] = ptmp[8 - 1 - i];
	}
	ptmp = (uint8 *)(&appnonce);
	for (i = 0; i<4; i++)
	{
		msg[i + 8] = ptmp[4 - 1 - i];
	}
	for (i = 0; i<4; i++)
	{
		msg[i + 12] = 0;
	}

	/*
	* aes_cmac 加密生成挑战字
	*/
	AES_CMAC_Init(&cmacctx);
	AES_CMAC_SetKey(&cmacctx, appkey);
	AES_CMAC_Update(&cmacctx, msg, 16);
	AES_CMAC_Final(tmp_challenge, &cmacctx);
	/*
	* 将挑战字转化为十六进制整数表示的字符串，(十六进制数字的字母部分采用大写，前面不加"0x")
	*/
	j = 0;
	for (i = 0; i<16; i++)
	{
		high = ((tmp_challenge[15 - i])&(0xF0)) >> 4;
		low = (tmp_challenge[15 - i])&(0x0F);
		if ((0 == flag) && ((0 == high) && (0 == low)))
		{
			continue;
		}
		if ((0 == flag) && (0 == high) && (0 != low))
		{
			if (low <= 9)
			{
				challenge[j] = '0' + low;
			}
			else
			{
				challenge[j] = 'A' + (low - 10);
			}
			j++;
			flag = 1;
			continue;
		}
		flag = 1;
		if (high <= 9)
		{
			challenge[j] = '0' + high;
		}
		else
		{
			challenge[j] = 'A' + (high - 10);
		}
		j++;
		if (low <= 9)
		{
			challenge[j] = '0' + low;
		}
		else
		{
			challenge[j] = 'A' + (low - 10);
		}
		j++;
	}
	challenge[32] = '\0';
#if 0
	FILE *fp;
	if (fp = fopen("challenge.dat", "wb"))
	{
		fwrite(challenge, 32, 1, fp);
		fclose(fp);
	}
	//memcpy(OutChallenge, challenge, 32);
#endif
}
