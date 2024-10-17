# How to Create and Use a Singularity Container With Apache-Jena-Fuseki

This guide provides instructions on how to build and run a Singularity container using the `playground.def` definition file. This container includes an Apache Jena Fuseki server configured with Java 22.

## Building the Container

Detailed information about building containers using Singularity can be found [here](https://docs.sylabs.io/guides/latest/user-guide/build_a_container.html).

### CLI Quick Reference

```
  # sudo singularity build --sandbox playground sif playground.def
  # sudo singularity shell --writable playground.sif/
  # $JENA_HOME/fuseki start
  # $JENA_HOME/fuseki stop
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

1. Navigate to the directory you want the container to reside in.
2. Use the command `vim playground.def` to create and enter an empty definition file.
   - **Note**: Use your preferred text editor. VIM is not required.
3. Copy and paste the contents of `playground.def` from this repo into the local copy of `playground.def` you just created and are currently editing. Save the file and quit, returning to the CLI.
   - Visit this [link](https://docs.sylabs.io/guides/latest/user-guide/definition_files.html) for more information on definition files.
4. Use the command `sudo singularity build --sandbox playground.sif playground.def` or, to build remotely, you can use
   - **Note**: This process can take up to several minutes to complete.
5. To enter the container use `sudo singularity shell --writable playground.sif` command. This "allows you to spawn a new shell within your container and interact with it as though it were a small virtual machine."
   - **Note**: One way to verify that you are inside a singularity container is by looking at the command prompt, which will display `Singularity>` or something similar to `root@DESKTOP-KE54U6:/usr/local/singularity#`.
6. Start the server using the command `$JENA_HOME/fuseki start`. This will create the /run directory and configuration files.
   - Use `$JENA_HOME/fuseki stop` to halt the server, before continuing.

### Configuring the Server

7. Navigate to the run folder inside the apache directory `cd /apache-jena-fuseki-5.0.0/run/`
8. Open the `shiro.ini` file
   - Comment out `/$/** = localhostFilter`
   - Where it says "allow any access" uncomment the line `/$/** = anon`
   - Add the following lines to file:
     ```
     /$/stats = anon
     /$/stats/* = anon
     ```
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
