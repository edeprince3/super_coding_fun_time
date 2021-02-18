#include"birds.hpp"

#include<string.h>
#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>

#include"GL/gl.h"
#include"GL/glut.h"
#include"GL/glu.h"


FlockingBirds::FlockingBirds(int n, double box_size) {

    n_ = n;

    n_target_ = 3;

    box_size_ = box_size;

    x_       = (double*)malloc(n_*sizeof(double));
    y_       = (double*)malloc(n_*sizeof(double));
    z_       = (double*)malloc(n_*sizeof(double));
    vx_      = (double*)malloc(n_*sizeof(double));
    vy_      = (double*)malloc(n_*sizeof(double));
    vz_      = (double*)malloc(n_*sizeof(double));
    ax_      = (double*)malloc(n_*sizeof(double));
    ay_      = (double*)malloc(n_*sizeof(double));
    az_      = (double*)malloc(n_*sizeof(double));
    ax_save_ = (double*)malloc(n_*sizeof(double));
    ay_save_ = (double*)malloc(n_*sizeof(double));
    az_save_ = (double*)malloc(n_*sizeof(double));

    memset((void*)x_      , '\0', n_*sizeof(double));
    memset((void*)y_      , '\0', n_*sizeof(double));
    memset((void*)z_      , '\0', n_*sizeof(double));
    memset((void*)vx_     , '\0', n_*sizeof(double));
    memset((void*)vy_     , '\0', n_*sizeof(double));
    memset((void*)vz_     , '\0', n_*sizeof(double));
    memset((void*)ax_     , '\0', n_*sizeof(double));
    memset((void*)ay_     , '\0', n_*sizeof(double));
    memset((void*)az_     , '\0', n_*sizeof(double));
    memset((void*)ax_save_, '\0', n_*sizeof(double));
    memset((void*)ay_save_, '\0', n_*sizeof(double));
    memset((void*)az_save_, '\0', n_*sizeof(double));

  
    // initial positions are random
    srand(time(0));
    for (int i = 0; i < n_; i++) {
        x_[i] = (double)rand()/RAND_MAX * box_size_;
        y_[i] = (double)rand()/RAND_MAX * box_size_;
        z_[i] = (double)rand()/RAND_MAX * box_size_;
    } 

    // initialize velocities are random
    for (int i = 0; i < n_; i++) {
        vx_[i] = ( (double)rand()/RAND_MAX - 0.5 ) * 2.0 * 0.05;
        vy_[i] = ( (double)rand()/RAND_MAX - 0.5 ) * 2.0 * 0.05;
        vz_[i] = ( (double)rand()/RAND_MAX - 0.5 ) * 2.0 * 0.05;
    } 

    dt_ = 0.05;

}

FlockingBirds::~FlockingBirds(){

    free(x_);
    free(y_);
    free(z_);
    free(vx_);
    free(vy_);
    free(vz_);
    free(ax_);
    free(ay_);
    free(az_);
    free(ax_save_);
    free(ay_save_);
    free(az_save_);
}

void FlockingBirds::update_flock() {

    double dt2 = dt_ * dt_;

    // x(t+dt) = x(t) + v(t) * dt + 1/2 a(t) * dt^2
    for (int i = n_target_; i < n_; i++) {
        x_[i] += vx_[i] * dt_ + 0.5 * ax_[i] * dt2;
        y_[i] += vy_[i] * dt_ + 0.5 * ay_[i] * dt2;
        z_[i] += vz_[i] * dt_ + 0.5 * az_[i] * dt2;

        // periodic boundary conditions!
        if ( x_[i] < 0.0 ) x_[i] += box_size_;
        if ( y_[i] < 0.0 ) y_[i] += box_size_;
        if ( z_[i] < 0.0 ) z_[i] += box_size_;

        if ( x_[i] > box_size_ ) x_[i] -= box_size_;
        if ( y_[i] > box_size_ ) y_[i] -= box_size_;
        if ( z_[i] > box_size_ ) z_[i] -= box_size_;

        ax_save_[i] = ax_[i];
        ay_save_[i] = ay_[i];
        az_save_[i] = az_[i];
    }

    for (int i = 0; i < n_target_; i++) {
        x_[i] += vx_[i] * dt_ + 0.5 * ax_[i] * dt2;
        y_[i] += vy_[i] * dt_ + 0.5 * ay_[i] * dt2;
        z_[i] += vz_[i] * dt_ + 0.5 * az_[i] * dt2;

        // periodic boundary conditions!
        if ( x_[i] < box_size_ ) x_[i] += box_size_;
        if ( y_[i] < box_size_ ) y_[i] += box_size_;
        if ( z_[i] < box_size_ ) z_[i] += box_size_;

        if ( x_[i] > box_size_ ) x_[i] -= box_size_;
        if ( y_[i] > box_size_ ) y_[i] -= box_size_;
        if ( z_[i] > box_size_ ) z_[i] -= box_size_;

        ax_save_[i] = ax_[i];
        ay_save_[i] = ay_[i];
        az_save_[i] = az_[i];
    }

    update_acceleration();

    // v(t+dt) = v(t) + ( a(t) + a(t+dt) ) * dt / 2
    for (int i = 0; i < n_; i++) {
        vx_[i] += 0.5 * (ax_[i] + ax_save_[i]) * dt_;
        vy_[i] += 0.5 * (ay_[i] + ay_save_[i]) * dt_;
        vz_[i] += 0.5 * (az_[i] + az_save_[i]) * dt_;
    }

    // enforce maximum velocity
    double max = 0.5;
    for (int i = 0; i < n_; i++) {
        double vx2 = vx_[i] * vx_[i];
        double vy2 = vy_[i] * vy_[i];
        double vz2 = vz_[i] * vz_[i];

        double v = sqrt(vx2 + vy2 + vz2);
        if ( v > max ) {
            vx_[i] *= max / v;
            vy_[i] *= max / v;
            vz_[i] *= max / v;
        }
    }


    print();

}

void FlockingBirds::update_acceleration() {

    memset((void*)ax_,'\0',n_*sizeof(double));
    memset((void*)ay_,'\0',n_*sizeof(double));
    memset((void*)az_,'\0',n_*sizeof(double));

    double halfbox = 0.5 * box_size_;

    double max_dist = box_size_ / 4.0;
    double min_dist = box_size_ / 6.0;

    for (int i = n_target_; i < n_; i++) {
        double xi = x_[i];
        double yi = y_[i];
        double zi = z_[i];
        for (int j = n_target_; j < n_; j++) {

            if ( i == j ) continue;

            double xj = x_[j];
            double yj = y_[j];
            double zj = z_[j];

            double dx = xi - xj;
            double dy = yi - yj;
            double dz = zi - zj;

            // minimum image convention
            if ( dx > halfbox ) {
                dx -= box_size_;
            }else if ( dx < -halfbox ) {
                dx += box_size_;
            }
            if ( dy > halfbox ) {
                dy -= box_size_;
            }else if ( dy < -halfbox ) {
                dy += box_size_;
            }
            if ( dz > halfbox ) {
                dz -= box_size_;
            }else if ( dz < -halfbox ) {
                dz += box_size_;
            }

            double r2 = dx*dx + dy*dy + dz*dz;
            double r = sqrt(r2);

            if ( r < max_dist && r > min_dist ) {

                double sx = dx / r;
                double sy = dy / r;
                double sz = dz / r;

                ax_[i] += -sx * 0.01;
                ay_[i] += -sy * 0.01;
                az_[i] += -sz * 0.01;

            }else if ( r < min_dist ) {

                double sx = dx / r;
                double sy = dy / r;
                double sz = dz / r;

                ax_[i] += sx * 0.01;
                ay_[i] += sy * 0.01;
                az_[i] += sz * 0.01;

            }

            
        }
    }


    // random nudge
    for (int i = 0; i < n_; i++) {
        double nudge_x = ( (double)rand()/RAND_MAX - 0.5 ) * 2.0;
        double nudge_y = ( (double)rand()/RAND_MAX - 0.5 ) * 2.0;
        double nudge_z = ( (double)rand()/RAND_MAX - 0.5 ) * 2.0;

        ax_[i] += nudge_x;
        ay_[i] += nudge_y;
        az_[i] += nudge_z;
    }

    for (int i = 0; i < n_target_; i++) {
        update_target_acceleration(i);
    }

}

void FlockingBirds::update_target_acceleration(int id) {

    double halfbox = 0.5 * box_size_;

    //double max_dist = box_size_ / 4.0;
    //double min_dist = box_size_ / 6.0;

    double xi = x_[id];
    double yi = y_[id];
    double zi = z_[id];

    ax_[id] = 0.0;
    ay_[id] = 0.0;
    az_[id] = 0.0;

    for (int j = n_target_; j < n_; j++) {

        double xj = x_[j];
        double yj = y_[j];
        double zj = z_[j];

        double dx = xi - xj;
        double dy = yi - yj;
        double dz = zi - zj;

        // minimum image convention
        if ( dx > halfbox ) {
            dx -= box_size_;
        }else if ( dx < -halfbox ) {
            dx += box_size_;
        }
        if ( dy > halfbox ) {
            dy -= box_size_;
        }else if ( dy < -halfbox ) {
            dy += box_size_;
        }
        if ( dz > halfbox ) {
            dz -= box_size_;
        }else if ( dz < -halfbox ) {
            dz += box_size_;
        }

        double r2 = dx*dx + dy*dy + dz*dz;
        double r = sqrt(r2);

        double sx = dx / r;
        double sy = dy / r;
        double sz = dz / r;

        double valx = sx * (box_size_ - r) / box_size_;
        double valy = sy * (box_size_ - r) / box_size_;
        double valz = sz * (box_size_ - r) / box_size_;

        ax_[id] -= -valx * 0.14;
        ay_[id] -= -valy * 0.14;
        az_[id] -= -valz * 0.14;

        ax_[j] -= -valx * 0.024 * (0.05 * n_);
        ay_[j] -= -valy * 0.024 * (0.05 * n_);
        az_[j] -= -valz * 0.024 * (0.05 * n_);

    }

    // random nudge
    double nudge_x = ( (double)rand()/RAND_MAX - 0.5 ) * 2.0;
    double nudge_y = ( (double)rand()/RAND_MAX - 0.5 ) * 2.0;
    double nudge_z = ( (double)rand()/RAND_MAX - 0.5 ) * 2.0;

    ax_[id] += nudge_x;
    ay_[id] += nudge_y;
    az_[id] += nudge_z;

}


void FlockingBirds::print() {

    double min  = 0.02 * box_size_ / 10.0;
    double size = 0.08 * box_size_ / 10.0;

    for (int i = 0; i < n_; i++) {

        double r = size * z_[i] / box_size_ + min;

        glColor3f(0.0,0.0,0.0);
        if ( i < n_target_ ) {
            glColor3f(1.0,0.0,0.0);
            r *= 2.0;
        }
        glBegin(GL_POLYGON);
            glVertex3f(x_[i],  y_[i],  z_[i]);
            glVertex3f(x_[i]+r,y_[i],  z_[i]);
            glVertex3f(x_[i]+r,y_[i]+r,z_[i]);
            glVertex3f(x_[i],  y_[i]+r,z_[i]);
        glEnd();
    }

    glFlush();
    glutSwapBuffers();
}
