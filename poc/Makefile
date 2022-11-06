
main: main.o fresnel.o single_film.o
	clang -o main main.o fresnel.o single_film.o

main.o: main.c
	clang ./main.c -o main.o -c

fresnel.o: fresnel.c
	clang ./fresnel.c -o fresnel.o -c

single_film.o: single_film.c
	clang ./single_film.c -o single_film.o -c

clean:
	rm *.o main
