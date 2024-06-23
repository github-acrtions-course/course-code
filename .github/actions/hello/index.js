import core from '@actions/core';
import github from '@actions/github';

try {

    core.debug("Hello, World!");
    core.warning("Watch out!");
    core.error("This is an error message");

    const name = core.getInput("who_to_greet");

    core.debug("Hello,  ${name}!");
    const time = new Date();
    core.setOutput("time", time.toTimeString());

    core.exportVariable("HELLO_TIME", time);    

    core.startGroup("Logging github context");
    console.log(JSON.stringify(github.context, null, 1));
    core.endGroup();
} catch (error) {
    core.setFailed(error.message);
}
