#ifndef __CHALLENGE_H__
#define __CHALLENGE_H__
#include "claa_base.h"
#define APPKEY_LEN (16)

void challenge_identification(uint8 appkey[APPKEY_LEN], uint64 appeui, uint32 appnonce,char*channel);
void get_challenge(char *appkey,char *appeui,uint32 appnonce, char *challenge);
#endif
