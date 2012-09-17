#include <stdio.h>

#include <gmp.h>
#include <mpfr.h>

#define LPREC 500

int main (void)
{
  unsigned int i;
  mpfr_t f, o;

  mpfr_init2 (f, LPREC);
  mpfr_set_d (f, 0.1, GMP_RNDD);

  mpfr_out_str (stdout, 10, 0, f, GMP_RNDD);
  putchar ('\n');

  mpfr_init2 (o, LPREC);
  mpfr_set_d (o, 2.0, GMP_RNDD);
  for (i = 0; i <= 1000000; i++)
    {
      mpfr_div (f, f, o, GMP_RNDD);
    }
  mpfr_out_str (stdout, 10, 0, f, GMP_RNDD);
  putchar ('\n');
  mpfr_clear (f);
  mpfr_clear (o);
  return 0;
}