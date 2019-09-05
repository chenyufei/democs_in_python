#include "challenge.h"
#include "claa_base.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
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
