#ifndef BIRDS_HPP
#define BIRDS_HPP

class FlockingBirds {

  public:

    // constructor
    FlockingBirds(int n, double box_size);

    // destructor
    ~FlockingBirds();

    // update flock via velocity verlet
    void update_flock();

    // box size
    double box_size() { return box_size_; }

  private:

    void print();

    int n_;

    int n_target_;

    double box_size_;

    // positions
    double * x_;
    double * y_;
    double * z_;

    // velocities
    double * vx_;
    double * vy_;
    double * vz_;

    // accelerations
    double * ax_;
    double * ay_;
    double * az_;

    // saved accelerations
    double * ax_save_;
    double * ay_save_;
    double * az_save_;

    // time step
    double dt_;

    // update acceleration
    void update_acceleration();

    // update target acceleration
    void update_target_acceleration(int id);


};

#endif
