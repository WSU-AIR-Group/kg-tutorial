# How to Create and Use a Singularity Container With Apache-Jena-Fuseki in Arsenal

This guide provides instructions on how to build and run a Singularity container using the `playground.def` definition file. This container includes an Apache Jena Fuseki server configured with Java 22, equipped with Jupyter Notebook and Firefox.

## Access With Singularity

### Create a Singularity Access Token for Remote Building

1. Create a Singularity account [here](https://cloud.sylabs.io).
2. Go to `access tokens` from the profile dropdown menu in the top right.
3. In the text bar, enter an alias for your token and hit `+Create Access Token`
4. Download a copy of this token and copy it to the clipboard for easy use in the following steps.
5. In the command line, type `singularity remote login`. Once the prompt appears to enter the access token, paste it into the terminal and hit enter. After a short while, there should be an output in the command line indicating the token has been verified along with its storage location.

### Generate Singularity Key Pair

```
# singularity keys newpair
# singularity keys list
# singularity keys push <paste-your-key-here>
```

1. In the CLI, use `singularity keys newpair`. This will generate a new key pair.
   - **Note**: When asked to enter your e-mail, ensure it is the same one attached to your Singularity account. Otherwise, you will not be properly verified when attempting to push your key.
2. Use the command `singularity keys list` to pull up a list of your keys. Identify the long string of characters (i.e. `D87FE3AF5C1F063FCBCC9B02F812842B5EEE5934`) and copy it.
3. Next, use `singularity keys push <paste-your-key-here>`. You should see a return output stating your public key was successfully pushed to the server.

## Building the Container

Detailed information about building containers using Singularity can be found [here](https://docs.sylabs.io/guides/latest/user-guide/build_a_container.html).

- **Note**: If using **Docker** instead of **Debootstrap** it is not necessary to build remotely since the arsenal server has the Docker package pre-installed.

### CLI Quick Reference

```
  # sudo singularity build --sandbox playground.sif playground.def
  # sudo singularity shell --writable playground.sif/
  # cd apache-jena-fuseki-5.0.0/run/
  # vim shiro.ini
      ## follow step 8
  # $JENA_HOME/fuseki start
  # $JENA_HOME/fuseki status
  # curl -X GET http://localhost:3030/$/server
  # $JENA_HOME/fuseki stop
```

### Guide and Explanation

To build a Singularity container from the `playground.def` file provided in this repo, follow these steps:

1. Navigate to your home directory on arsenal.
2. Use the command `vim playground.def` to create and enter the necessary definition file for singularity to build an image.
   - **Note**: Use your preferred text editor. VIM is not required.
3. Copy and paste the contents of `playground.def` from this repo into the local copy of `playground.def` you just created and are currently editing. Save the file and quit, returning to the CLI.
   - Visit this [link](https://docs.sylabs.io/guides/latest/user-guide/definition_files.html) for more information on definition files.
4. Use the command `sudo singularity build --sandbox playground.sif playground.def` or, to build remotely, you can use
   `singularity build --remote --sandbox --fakeroot playground.sif playground.def` to build the container.
   - **Note**: This process can take up to several minutes to complete.
5. To enter the container use `sudo singularity shell --writable playground.sif` command. This "allows you to spawn a new shell within your container and interact with it as though it were a small virtual machine."
   - **Note**: One way to verify that you are inside a singularity container is by looking at the command prompt, which will display `Singularity>` or something similar to `root@DESKTOP-KE54U6:/usr/local/singularity#`.
6. Start the server using the command `$JENA_HOME/fuseki start`. This will create the /run directory and configuration files.
   - Use `$JENA_HOME/fuseki stop` to halt the server, before continuing.

### Configuring the Server

7. Navigate to the run folder inside the apache directory `cd /apache-jena-fuseki-5.0.0/run/`
8. Open the `shiro.ini` file
   - Comment out `/$/** = localhostFilter`
   - Where it says "allow any access" uncomment the line `/$/** = anon` and add the following: `/$/stats = anon` and `/$/stats/* = anon`
   - Save and exit file

### Starting the Server

**Note:** If using a specific port for your jena fuseki server use the command in step 10.

9. While inside the container you can use `$JENA_HOME/fuseki start` to start up the apache-jena-fuseki server.
   - To verify the server is running correctly, do the following: `$JENA_HOME/fuseki status`, and the output should say if Fuseki is running and give its PID.
   - Additionally, you can use the curl command `curl -X GET http://localhost:3030/$/server`, which will output information about the server in JSON format.
   - Another way to verify the server is to go to use the command `hostname -I` to see the Arsenal server's IP address. In your browser, type in http://ip-address-here:3030. The apache-jena-fuseki webpage should appear and can be interacted with. - **Note**: If two IP addresses appear, use the one on the right.
10. If a specific port is required use the following command `java -Xmx1200M -jar fuseki-server.jar --port=8005`

- If using this method use `http://ip-address-here:PORT#`

11. To stop the server, use the command `$JENA_HOME/fuseki stop`

## Using Jupyter Notebook in a Singularity Container

```
# cd /root/jupyter-notebooks
# jupyter notebook --no-browser --allow-root --port=5000 > jupyter.out 2> jupyter.err &
# jupyter notebook list
```

1. Navigate to the jupyter directory `cd /root/jupyter-notebooks`
2. Activate server hosting with Jupyter `jupyter notebook --no-browser --allow-root --port=5000 > jupyter.out 2> jupyter.err &`
   - This will run the Jupyter server in the background on port 5000
3. To view the available URL's `jupyter notebook list`
4. Copy and paste the URL from `:: /root/jupyter-notebooks` into your browser to gain access to jupyter notebooks features.

## Stopping Jupyter Notebooks Server

```
# ps
# kill <pid-here>
```

1. Use the command `ps` to display the processes that are currently running. Look for the PID next to "jupyter-noteboo".
2. use the command `kill <pid-here>`
