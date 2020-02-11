#include "gtest/gtest.h"

// ForceField t;
// t.token_x_prime[0].op = mtCONST;
// t.token_x_prime[0].value = 1;
// t.token_x_prime[1].op = mtVAR;
// t.token_x_prime[1].value = 1;
// t.token_x_prime[2].op = mtADD;
// t.token_x_prime[3].op = mtSIN;
// t.token_x_prime[4].op = mtVAR;
// t.token_x_prime[4].value = 0;
// t.token_x_prime[5].op = mtADD;
// t.token_x_prime[6].op = mtEND;

// t.token_y_prime[0].set(mtVAR, 1);
// t.token_y_prime[1].set(mtVAR, 0);
// t.token_y_prime[2].set(mtCONST, 0.2f);
// t.token_y_prime[3].set(mtVAR, 2);
// t.token_y_prime[4].set(mtSIN);
// t.token_y_prime[5].set(mtCONST, 0.1);
// t.token_y_prime[6].set(mtSUB);
// t.token_y_prime[7].set(mtCOS);
// t.token_y_prime[8].set(mtMUL);
// t.token_y_prime[9].set(mtMUL);
// t.token_y_prime[10].set(mtADD);
// t.token_y_prime[11].set(mtEND);

// t.token_z_prime[0].set(mtPI);
// t.token_z_prime[1].set(mtCONST, 10);
// t.token_z_prime[2].set(mtMUL);
// t.token_z_prime[3].set(mtINT);
// t.token_z_prime[4].set(mtEND);

// if (!t.validate()) {
//     printf("formula validation failed.\n");
//     return 1;
// }

// double ret = t.z_prime(0.32, 1.5, 3, 0.2);

// ForceField *d_t;
// cudaMalloc(&d_t, sizeof(ForceField));
// cudaMemcpy(d_t, &t, sizeof(ForceField), cudaMemcpyHostToDevice);
// kernel<<<1, 1>>>(d_t);
// cudaDeviceSynchronize();

// printf("in host: %f\n", ret);