//
//  main.c
//  Data Structure
//  Array insertion at front of array
//  Created by Ayush Borade on 09/01/25.
//

#include <stdio.h>
int main(void){
    int n,i;
    printf("Enter no. of elements in array:");
    scanf("%d",&n);
    int a[n];
    for (i=0; i<n; i++) {
        printf("Enter element a[%d]:",i);
        scanf("%d",&a[i]);
    }
    printf("Array before insertion:\n");
    for (i=0; i<n; i++) {

        printf("a[%d]= %d\n",i,a[i]);
    }
    n++;
    for (i=n; i>=0; i--) {
        a[i+1]=a[i];
    }
    printf("Enter the element to insert at front:");
    scanf("%d",&a[0]);
    printf("Array after insertion:\n");
    for (i=0; i<n; i++) {
        printf("a[%d]= %d\n",i,a[i]);
    }
    return 0;
}
