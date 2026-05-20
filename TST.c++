#include <stdio.h>

#define N 3

void gaussSeidel(double a[N][N+1]) {
    double x[N] = {0};
    int maxIter = 100;
    double tol = 0.0001;

    for (int iter = 0; iter < maxIter; iter++) {
        double xOld[N];
        for (int i = 0; i < N; i++)
            xOld[i] = x[i];

        for (int i = 0; i < N; i++) {
            double sum = 0;
            for (int j = 0; j < N; j++) {
                if (j != i)
                    sum += a[i][j] * x[j];
            }
            x[i] = (a[i][N] - sum) / a[i][i];
        }

        int converged = 1;
        for (int i = 0; i < N; i++) {
            if (fabs(x[i] - xOld[i]) > tol) {
                converged = 0;
                break;
            }
        }
        if (converged) {
            printf("Solution converged:\n");
            for (int i = 0; i < N; i++)
                printf("x%d = %f\n", i, x[i]);
            return;
        }
    }
    printf("Did not converge\n");
}

int main() {
    double a[N][N+1] = {
        {4, 1, -1, 3},
        {1, 4, 1, 6},
        {-1, 1, 3, -6}
    };
    gaussSeidel(a);
    return 0;
}