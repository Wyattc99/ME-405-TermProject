# Term Project Proposal
## Authors: Wyatt Conner, Jameson Spitz, Jacob Wong

#Introduction
Our system will be able to draw a picture roughly 4" x 6" in size by having our Nucleo 
microcontroller drive two motors to move a pencil along 2 axis. Additionally, the system 
must have some functionality to raise the pencil slightly off the paper when not drawing.

To accomplish this, we will be using a lead screw to allow the pencil to slide one direction
along the paper. This lead screw will be driven by a motor coupled to the lead screw. 
Additionally, the pencil will be secured in a housing that is secured to the lead screw. The 
pencil is intened to be raised and lowered by a solenoid stored in the housing. In addition 
to the lead screw, our system will rotate in the theta direction by a shaft connected to a 
pin joint at the center of the arc. A second motor is secured to the shaft, which drives a
wheel to rotate the shaft about the pin joint. Connecting the pencil housing to the shaft,
we will 3D print a clip to slide along the shaft. With the motor controlled lead screw and 
shaft, our pencil can move anywhere in the radial and theta direction. All parts will be
either bought online, 3D printed, or found in our local Cal Poly machine shops.


#Bill Of Materials


| Qty. | Part                    | Source                | Est. Cost |
|:----:|:----------------------  |:----------------------|:---------:|
|  1   | Wheel                   | Caster HQ             |   $6.59   |
|  1   | Rod End                 | MiSumi                |   $9.95   |
|  1   | Lead Screw              | Amazom                |   $12.99  |
|  1   | Solenoid                | Digi-Key              |   $4.95   |
|  1   | Shaft Slider            | 3D Printing           |     -     |
|  1   | Pencil/Solenoid Housing | 3D Printing           |     -     |
|  1   | Electrical Tape         | Home                  |     -     |
|  3   | Zip Ties                | Home                  |     -     |
|  5   | Wires/Solder            | ME 405 Lab            |     -     |
|  2   | Motors                  | ME 405 Lab            |     -     |
|  1   | Wood Block              | Dumpster Behind Bondo | Our pride |
|  1   | Shaft                   | Dumpster Behind Bondo | Our Pride |
|  1   | 9.6mm Fitting           | Dumpster Behind Bondo | Our pride |
|  1   | Pin Joint               | Dumpster Behind Bondo | Our pride |

#CAD Model

### Assembly Drawing and BOM
![RC Circuit Wiring](/images/RC_Circuit.png)