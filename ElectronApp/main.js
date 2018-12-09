const { app, BrowserWindow, ipcMain } = require('electron');
const { createPythonBridge } = require("./background/pythonbridge.js");
const { invertObject } = require("./shared/utils.js");

let activeWindow, pythonBridge;
//Command names to send and receive from the python
const actionNameMappings = {
    "toggle_stacktrace": "toggleStacktrace",
    "create_new": "create",
    "load_from_file": "load",
    "save_to_file": "save",
    "add_fully_connected_layer": "addFullyConnectedLayer",
    "add_conv_1d_layer": "addConv1DLayer",
    "remove_layer": "removeLayer",
    "train_network": "train",
    "retrieve_current_network_data": "retrieve",
    "get_weight_matrix": "getWeightMatrix",
    "resize_layer": "resizeLayer"
};
const invertedActionNameMappings = invertObject(actionNameMappings);
//Creatges the main window
function createWindow() {
    if (activeWindow !== undefined) {
        activeWindow.close();
    }
    //instantiates the main browser window at the specified width and height
    activeWindow = new BrowserWindow({ width: 800, height: 600 });
    //loads the starting renderer page
    activeWindow.loadFile('render/views/index.html');

    // Emitted when the window is closed.
    activeWindow.on('closed', () => {
        activeWindow = undefined;
    });
}
//Handler for when a python message arrives
function onPythonMessage(message) {
    //Checks to make sure there is an active window
    if (activeWindow === undefined) {
        console.error("No active window");
        return;
    }

    let commaIndex = message.indexOf(",");
    let actionName = message.substring(0, commaIndex);
    let responseObject = JSON.parse(message.substring(commaIndex + 1));
    //Makes sure the messsage received didn't error
    if (responseObject.statusCode > 0) {
        console.error(message);
        return;
    }
    //Checks to see if the action is a used name
    if (!(actionName in actionNameMappings)) {
        console.error("Unrecognized action name: " + actionName);
        return;
    }
    //sends the python object to the renderer process
    activeWindow.webContents.send('async-reply', actionNameMappings[actionName], responseObject);
}

//Listener to call various python scripts
ipcMain.on('async', (event, requestedAction, ...args) => {
    let actionName = invertedActionNameMappings[requestedAction];
    pythonBridge.sendMessage(actionName + " " + args.join(" "));
});

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', () => {
    pythonBridge = createPythonBridge(onPythonMessage, '../PythonApp/main.py');
    pythonBridge.sendMessage("toggle_stacktrace");
    createWindow();
});

// Quit when all windows are closed.
app.on('window-all-closed', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
//Kills the python bridge before quitting the application
app.on('before-quit', () => {
    if (pythonBridge !== undefined) {
        console.log("Killing python bridge");
        pythonBridge.sendMessage("quit");
        pythonBridge = undefined;
    }
});

app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (activeWindow === null) {
        createWindow();
    }
})
console.log("Launching Neural Ninja Application");