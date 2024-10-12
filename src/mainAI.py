self.prev_distance = distVector.magnitude()
        

        if distVector.magnitude() < self.prev_distance:
            self.prev_distance = distVector.magnitude()
            Reward += int((self.car.velocity.magnitude()))* 100
        else:
            Reward -= 10


        vec1 = (self.target_point-self.car.position)
        vec2 = (self.car.dir- self.car.position)
        cangle = vec1.angle_between(vec2)

        Reward += (int(self.prev_rot - cangle)/10)

        if (self.check_done()):
            Reward += 1000

        Reward -= (distVector.magnitude()/5)
