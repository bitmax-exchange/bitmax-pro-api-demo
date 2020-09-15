#include "bitmax_util.h"


string b2a_hex( char *byte_arr, int n ) {

    const static std::string HexCodes = "0123456789abcdef";
    string HexString;
    for ( int i = 0; i < n ; ++i ) {
        unsigned char BinValue = byte_arr[i];
        HexString += HexCodes[( BinValue >> 4 ) & 0x0F];
        HexString += HexCodes[BinValue & 0x0F];
    }
    return HexString;
}

string hmac_sha256(string key, string data) {
  char hmac_key_buf[100];
  int key_len = EVP_DecodeBlock((unsigned char*)hmac_key_buf, (unsigned char*)key.c_str(),  key.length());
  string hmac_key = key; // string(hmac_key_buf, key_len); //base64_decode_str(key);
  const unsigned char* digest = HMAC(EVP_sha256(), hmac_key.c_str(), strlen(hmac_key.c_str()), (unsigned char*)data.c_str(), data.length(), NULL, NULL);  
  //signature buf afer hmac and base64
  char signature[100];
  EVP_EncodeBlock((unsigned char *) signature, digest, strlen((const char*)digest));
  return signature;
  //string digest_str = string((const char*)digest, strlen((const char*)digest));
  //return base64_encode_str(digest_str);
}   

string hmac_sha256_binance( const char *key, const char *data) {
    string hmac_key = string(key, strlen(key)); // base64_decode((const unsigned char*)key, strlen(key)); //
    //const unsigned char* digest = HMAC(EVP_sha256(), key, strlen(key), (unsigned char*)data, strlen(data), NULL, NULL);  
    const unsigned char* digest = HMAC(EVP_sha256(), hmac_key.c_str(), strlen(hmac_key.c_str()), (unsigned char*)data, strlen(data), NULL, NULL);  

    return  b2a_hex( (char *)digest, 32 ); //base64_encode((const unsigned char *)digest, strlen((const char*)digest));
}   

