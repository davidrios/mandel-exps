/**  mandel.c   by Eric R. Weeks   written 9-28-96
 **  weeks@physics.emory.edu
 **  http://www.physics.emory.edu/~weeks/
 **  
 **  This program is public domain, but this header must be left intact
 **  and unchanged.
 **  
 **  to compile:  cc -o mand mandel.c
 ** 
 **/

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
 
void mandel(char* out, int res, int itermax, double magnify)
{
    double x,xx,y,cx,cy;
    int iteration,hx,hy;
    int hxres = res;                /* horizonal resolution         */
    int hyres = res;                /* vertical resolution          */
    char* outPtr = out;

    outPtr += sprintf(outPtr, "P5\n%d %d\n255\n", hxres, hyres);

    for (hy=1;hy<=hyres;hy++)  {
        for (hx=1;hx<=hxres;hx++)  {
            cx = (((float)hx)/((float)hxres)-0.5)/magnify*3.0-0.7;
            cy = (((float)hy)/((float)hyres)-0.5)/magnify*3.0;
            x = 0.0; y = 0.0;
            for (iteration=1;iteration<itermax;iteration++)  {
                xx = x*x-y*y+cx;
                y = 2.0*x*y+cy;
                x = xx;
                if (x*x+y*y>100.0)  iteration = 999999;
            }
            if (iteration<99999) outPtr += sprintf(outPtr, "%c", 1);
            else outPtr += sprintf(outPtr, "%c", 255);
        }
    }
}
