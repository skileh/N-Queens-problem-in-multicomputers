#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <sys/time.h>

#include <omp.h>

#define MAX_N 16

//export OMP_NUM_THREADS=<numero de threads>
//gcc -fopenmp nqueen.c -o nqueen
//./nqueen n

int verifica(int linha_rainha[MAX_N], int n)
{
	int i, j;
	for (i = 0; i < n; i++)
	{
		for (j = i+1; j < n; j++)
		{
			// two queens in the same row => not a solution!
			if (linha_rainha[i] == linha_rainha[j]) return 0;

			// two queens in the same diagonal => not a solution!
			if (linha_rainha[i] - linha_rainha[j] == i - j ||
			    linha_rainha[i] - linha_rainha[j] == j - i)
			    return 0;
		}
	}

	return 1;
}

int mainC(int n, int num_pc)
{	
    long num_iteracao = 1,iter;

    double inicio_tempo, fim_tempo;
    int number_solutions = 0;
	int num_threads;
    int i, ini_iteracao, fim_iteracao;

    num_threads = 8; 

    omp_set_num_threads(num_threads);

		//for para saber quantas iterações maximas existem
    for (i = 0; i < n; i++)
    {
        num_iteracao *= n;
    }

		//calculo inicial do tempo
    inicio_tempo = omp_get_wtime();

    //divide o numero de operações
    if(num_pc==1){
    	ini_iteracao = 0;
    	fim_iteracao = num_iteracao*0.25;
    }
    else if(num_pc==2){
    	ini_iteracao = num_iteracao*0.25;
    	fim_iteracao = num_iteracao*0.5;

    }
    else if(num_pc==3){
    	ini_iteracao = num_iteracao*0.5;
    	fim_iteracao = num_iteracao*0.75;
    }
    else{
    	ini_iteracao = num_iteracao*0.75;
    	fim_iteracao = num_iteracao;
    }


	//printf("Número de threads max: %d\n", omp_get_max_threads());
	#pragma omp parallel for reduction (+:number_solutions)
	for (iter = ini_iteracao; iter < fim_iteracao; iter++)
	{
		//printf("\nNúmero de threads: %d\n", omp_get_num_threads());
		long code = iter;
		int i;
	  	int linha_rainha[MAX_N];

		// o indice do vetor corresponde ao numero e coluna da rainha
		// apenas geramos configurações onde há apenas uma rainha por coluna
		for (i = 0; i < n; i++)
		{
			linha_rainha[i] = code % n;

			code /= n;
		}

		if (verifica(linha_rainha, n))
		{
		    number_solutions++;
		}
	}

    // calculo tempo final
    fim_tempo = omp_get_wtime();

    // print resultados
    //printf("The execution time is %g sec\n", fim_tempo - inicio_tempo);
    //printf("Number of found solutions is %d\n", number_solutions);
	return number_solutions;
}