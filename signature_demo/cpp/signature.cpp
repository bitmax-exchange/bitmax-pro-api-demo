#include "bitmax_util.h"


int main(){
    // string APIKey = "";
    string secret_key = "98dRnVqbIhriRMZJfax3EvSPRBJrIuZ6J755KcLz6napGUpzmApJmfBY7EY3yYZn";
    
    // chrono::milliseconds ms = chrono::duration_cast< chrono::milliseconds >(chrono::system_clock::now().time_since_epoch());
    long timestamp = 1562952827927000L; // Please use the same timestamp (in milliseconds) as in request header.

    string msg = to_string(timestamp) + "+user/info";
    string signature = hmac_sha256(secret_key, msg);

    printf("Prehash msg: %s\n", msg.c_str());
    printf("Signature: %s\n", signature.c_str());


}