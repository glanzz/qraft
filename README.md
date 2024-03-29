# QRAFT

### Reverse Your Quantum Circuit and Know the Correct Program Output
###### Authored By: Tirthak Patel and Devesh Tiwari
###### Implemented By: Bhargav C N
##### [Documentation](https://par.nsf.gov/servlets/purl/10309262)
Requires:
pip 24.0
Python 3.12.2
<br/>
<br/>

## Installation

Create virtual environment
<pre>python3 -m virtualenv venv</pre>
Activate virtual environment
<pre>source venv/bin/activate</pre>
Install requirements
<pre>pip install -r requirements.txt</pre>

<br/>

### Usage
- Clone the repository and Make sure you to finish the installation process mentioned above
- Generate random circuits data for testing and training <pre>python qraft-gen/generate_data.py</pre> 
- You can change the params before run in `qraft-gen/generate_data.py` file like total number of circuits and simulations per circuit ( These params are in all-caps) you can also change the file name
- After the data is generated use it as the input to the training and testing model
<pre>python qraft-predict/train.py</pre>
This requires the data generated from the previous step
- After successful execution of the above command. The model would be present as `qraft-1.pkl`
- Test the model using the following command:
<pre>python qraft-predict/predict.py</pre>
- You can also use the data generator to generate datasets for predicting by altering the `TOTAL_CIRCUITS_REQUIRED`
- Examine the accuracy of your circuit using 
<pre>python qraft-gen/examine_circuit.py</pre>
This provides three graphs which provides insights on the model prediction which is corrected true state probability



### Modules Description
- `qraft-gen`: Module that generates random quantum circuits for training and testing data
- `qraft-predict`: Module that generates the QRAFT core model using the generated data






### Outputs

One of the FC & FRC circuit generated by circuit generator
<pre>
     ┌────────────┐    ┌───────────┐    ┌───────────┐
q_0: ┤ U1(5.2566) ├────┤ U1(2.455) ├────┤ U1(2.636) ├
     └───┬───┬────┘┌───┴───────────┴───┐└───────────┘
q_1: ────┤ X ├─────┤ U2(0.776,0.66403) ├──────■──────
         └─┬─┘     └──┬─────────────┬──┘    ┌─┴─┐    
q_2: ──────■──────────┤ U1(0.26441) ├───────┤ X ├────
                      └─────────────┘       └───┘    
     ┌────────────┐    ┌───────────┐    ┌───────────┐┌───────────┐    ┌───────────┐    ┌────────────┐
q_0: ┤ U1(5.2566) ├────┤ U1(2.455) ├────┤ U1(2.636) ├┤ U1(2.636) ├────┤ U1(2.455) ├────┤ U1(5.2566) ├
     └───┬───┬────┘┌───┴───────────┴───┐└───────────┘└───────────┘┌───┴───────────┴───┐└───┬───┬────┘
q_1: ────┤ X ├─────┤ U2(0.776,0.66403) ├──────■────────────■──────┤ U2(0.776,0.66403) ├────┤ X ├─────
         └─┬─┘     └──┬─────────────┬──┘    ┌─┴─┐        ┌─┴─┐    └──┬─────────────┬──┘    └─┬─┘     
q_2: ──────■──────────┤ U1(0.26441) ├───────┤ X ├────────┤ X ├───────┤ U1(0.26441) ├─────────■───────
                      └─────────────┘       └───┘        └───┘       └─────────────┘                 

</pre>


![State_error](https://github.com/glanzz/qraft/assets/60913501/ed31ede4-8274-49e5-8a5d-9701f09276c7)
![Dominant_state_error](https://github.com/glanzz/qraft/assets/60913501/aae88275-c70a-49ca-a6dc-576254d9882d)
![Program_error](https://github.com/glanzz/qraft/assets/60913501/44eb6ff7-8a52-4769-8678-4c41ea5bef1b)
