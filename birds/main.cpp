#include<stdio.h> 
#include<memory>

// OpenGL headers
#include<GL/gl.h>
#include<GL/glu.h>
#include<GL/glut.h>

#include"birds.hpp"

std::shared_ptr<FlockingBirds> birds;

// display function
void display(void){

    glClear(GL_COLOR_BUFFER_BIT);

    birds->update_flock();


}


void idle(){
  glutPostRedisplay();
  glFlush();
}


int main(int argc, char** argv){

    birds = (std::shared_ptr<FlockingBirds>)(new FlockingBirds(1000.0,10.0));

    glutInit(&argc,argv);

    glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH );
    glutInitWindowSize(800,800);
    glutInitWindowPosition(3100,0);
    glutCreateWindow("birds!");

    // select background color
    glClearColor(1.0,1.0,1.0,0.0);

    // initialize viewing values
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    double box = birds->box_size();

    // box viewing values
    glOrtho(-0.1*box,1.1*box,-0.1*box,1.1*box,-1.0*box,2.0*box);

    // define display function
    glutDisplayFunc(display);
    glutIdleFunc(idle);

    glutMainLoop();
  

    return 0; 
}

