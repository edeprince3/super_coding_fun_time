LIB       = -L/usr/lib/x86_64-linux-gnu/ -lglut -lGL -lGLU
INCLUDE   = -I/usr/include
CFLAGS    = -O2 
FFLAGS    = -O2 
EXEC      = birds.x 
CXX       = g++

$(EXEC): main.cpp birds.o 
	$(CXX) main.cpp birds.o $(CFLAGS) $(INCLUDE) $(LIB) -o $(EXEC)

birds.o: birds.cpp birds.hpp
	$(CXX) -c birds.cpp $(CFLAGS) $(INCLUDE)

clean:
	rm -f *.o *.x
