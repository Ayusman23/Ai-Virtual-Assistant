$(document).ready(function () {

    // 1. Initialize Assistant (Face Auth, Device check)
    eel.initializeAssistant()();

    // 2. Text Animations (Ask me anything)
    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },
    });

    // 3. Siri Wave Configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart: true
    });

    // 4. Siri Message Animation (Listening...)
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
            callback: function () {
                $('.siri-message').textillate('in');
            }
        },
    });

    // 5. Microphone Button Click
    $("#MicBtn").click(function () {
        eel.playAssistantSound();
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()();
    });

    // 5.1 Stop Button Click
    $("#StopBtn").click(function () {
        eel.stopSpeaking()();
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    });

    // 6. Keyboard Shortcut (Ctrl+J or Cmd+J)
    function doc_keyUp(e) {
        if (e.key === 'j' && (e.metaKey || e.ctrlKey)) {
            eel.playAssistantSound();
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()();
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // 7. Helper: Play Assistant (Send Text)
    function PlayAssistant(message) {
        if (message != "") {
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("");
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
    }

    // 8. Toggle Mic/Send Button based on input
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        } else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    $("#chatbox").keyup(function () {
        let message = $("#chatbox").val();
        ShowHideButton(message);
    });

    $("#SendBtn").click(function () {
        let message = $("#chatbox").val();
        PlayAssistant(message);
    });

    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val();
            PlayAssistant(message);
        }
    });

    // --- SETTINGS SECTION ---

    // Load initial data
    eel.personalInfo()();
    eel.displaySysCommand()();
    eel.displayWebCommand()();
    eel.displayPhoneBookCommand()();

    // A. Personal Info Logic
    eel.expose(getData);
    function getData(user_info) {
        try {
            let data = JSON.parse(user_info);
            let idsPersonalInfo = ['OwnerName', 'Designation', 'MobileNo', 'Email', 'City'];
            let idsInputInfo = ['InputOwnerName', 'InputDesignation', 'InputMobileNo', 'InputEmail', 'InputCity'];

            for (let i = 0; i < data.length; i++) {
                let hashid = "#" + idsPersonalInfo[i];
                $(hashid).text(data[i]);
                $("#" + idsInputInfo[i]).val(data[i]);
            }
        } catch (e) {
            console.error("Error parsing user info:", e);
        }
    }

    $("#UpdateBtn").click(function () {
        let OwnerName = $("#InputOwnerName").val();
        let Designation = $("#InputDesignation").val();
        let MobileNo = $("#InputMobileNo").val();
        let Email = $("#InputEmail").val();
        let City = $("#InputCity").val();

        if (OwnerName && Designation && MobileNo && Email && City) {
            eel.updatePersonalInfo(OwnerName, Designation, MobileNo, Email, City);
            swal({
                title: "Updated Successfully",
                icon: "success",
            });
        } else {
            // Ensure you have a toast element in HTML or use simple alert
            alert("All Fields Mandatory");
        }
    });

    // B. System Commands Logic
    eel.expose(displaySysCommand);
    function displaySysCommand(array) {
        try {
            let data = JSON.parse(array);
            let placeholder = document.querySelector("#TableData");
            let out = "";
            for (let i = 0; i < data.length; i++) {
                out += `
                    <tr>
                        <td class="text-light">${i + 1}</td>
                        <td class="text-light">${data[i][1]}</td>
                        <td class="text-light">${data[i][2]}</td>
                        <td class="text-light">
                            <button id="${data[i][0]}" onClick="SysDeleteID(this.id)" class="btn btn-sm btn-danger">Delete</button>
                        </td>
                    </tr>
                `;
            }
            placeholder.innerHTML = out;
        } catch (e) {
            console.log("No system commands found or error parsing.");
        }
    }

    $("#SysCommandAddBtn").click(function () {
        let key = $("#SysCommandKey").val();
        let value = $("#SysCommandValue").val();

        if (key.length > 0 && value.length > 0) {
            eel.addSysCommand(key, value)(function () {
                // Refresh ONLY after addition is confirmed
                eel.displaySysCommand()();
            });

            swal({
                title: "Added Successfully",
                icon: "success",
            });
            $("#SysCommandKey").val("");
            $("#SysCommandValue").val("");
        } else {
            alert("All Fields Mandatory");
        }
    });

    // C. Web Commands Logic
    eel.expose(displayWebCommand);
    function displayWebCommand(array) {
        try {
            let data = JSON.parse(array);
            let placeholder = document.querySelector("#WebTableData");
            let out = "";
            for (let i = 0; i < data.length; i++) {
                out += `
                    <tr>
                        <td class="text-light">${i + 1}</td>
                        <td class="text-light">${data[i][1]}</td>
                        <td class="text-light">${data[i][2]}</td>
                        <td class="text-light">
                            <button id="${data[i][0]}" onClick="WebDeleteID(this.id)" class="btn btn-sm btn-danger">Delete</button>
                        </td>
                    </tr>
                `;
            }
            placeholder.innerHTML = out;
        } catch (e) {
            console.log("No web commands found.");
        }
    }

    $("#WebCommandAddBtn").click(function () {
        let key = $("#WebCommandKey").val();
        let value = $("#WebCommandValue").val();

        if (key.length > 0 && value.length > 0) {
            eel.addWebCommand(key, value)(function () {
                eel.displayWebCommand()();
            });

            swal({
                title: "Added Successfully",
                icon: "success",
            });
            $("#WebCommandKey").val("");
            $("#WebCommandValue").val("");
        } else {
            alert("All Fields Mandatory");
        }
    });

    // D. Phone Book Logic
    eel.expose(displayPhoneBookCommand);
    function displayPhoneBookCommand(array) {
        try {
            let data = JSON.parse(array);
            let placeholder = document.querySelector("#ContactTableData");
            let out = "";
            for (let i = 0; i < data.length; i++) {
                out += `
                    <tr>
                        <td class="text-light">${i + 1}</td>
                        <td class="text-light">${data[i][1]}</td>
                        <td class="text-light">${data[i][2]}</td>
                        <td class="text-light">${data[i][3]}</td>
                        <td class="text-light">${data[i][4]}</td>
                        <td class="text-light">
                            <button id="${data[i][0]}" onClick="ContactDeleteID(this.id)" class="btn btn-sm btn-danger">Delete</button>
                        </td>
                    </tr>
                `;
            }
            placeholder.innerHTML = out;
        } catch (e) {
            console.log("No contacts found.");
        }
    }

    $("#AddContactBtn").click(function () {
        let Name = $("#InputContactName").val();
        let MobileNo = $("#InputContactMobileNo").val();
        let Email = $("#InputContactEmail").val();
        let City = $("#InputContactCity").val();

        if (Name.length > 0 && MobileNo.length > 0) {
            eel.InsertContacts(Name, MobileNo, Email, City)(function () {
                eel.displayPhoneBookCommand()();
            });

            swal({
                title: "Added Successfully",
                icon: "success",
            });

            $("#InputContactName").val("");
            $("#InputContactMobileNo").val("");
            $("#InputContactEmail").val("");
            $("#InputContactCity").val("");
        } else {
            alert("Name and Mobile Number are Mandatory");
        }
    });

    // Consolidated Upload Logic
    $("#FileSelection").change(function (e) {
        let files = e.target.files;
        if (files.length === 0) return;

        if (files.length > 1) {
            // Treat as a Folder
            let folderName = files[0].webkitRelativePath.split('/')[0] || "Selected Files";
            let fileList = [];
            for (let i = 0; i < files.length; i++) {
                fileList.push(files[i].webkitRelativePath || files[i].name);
            }
            eel.analyzeFolder(folderName, fileList)();
            swal({ title: "Analyzing Content", text: `Analyzing ${files.length} items...`, icon: "info" });
        } else {
            // Single File or Image
            let file = files[0];
            let reader = new FileReader();
            if (file.type.startsWith("image/")) {
                reader.onload = function (event) {
                    eel.analyzeImage(event.target.result, file.type)();
                    swal({ title: "Analyzing Image", text: "Processing with Vision AI...", icon: "info" });
                };
                reader.readAsDataURL(file);
            } else {
                reader.onload = function (event) {
                    eel.analyzeFile(file.name, event.target.result)();
                    swal({ title: "Analyzing File", text: `Reading ${file.name}...`, icon: "info" });
                };
                reader.readAsText(file);
            }
        }
    });

    // F. Face Training Logic
    $("#TrainFaceBtn").click(function () {
        swal({
            title: "Start Training?",
            text: "This will open your camera to capture and train your face data.",
            buttons: true,
            icon: "warning"
        }).then((willTrain) => {
            if (willTrain) {
                eel.trainFaceRecognition()();
            }
        });
    });

});

// --- GLOBAL FUNCTIONS (Must be outside $(document).ready for onClick access) ---

// 1. System Delete - FIXED WITH CALLBACK
function SysDeleteID(clicked_id) {
    // We pass a callback function inside .then() or as an argument to wait for Python
    eel.deleteSysCommand(clicked_id)(function () {
        // This runs ONLY after Python finishes deleting
        eel.displaySysCommand()();
    });
}

// 2. Web Delete - FIXED WITH CALLBACK
function WebDeleteID(clicked_id) {
    eel.deleteWebCommand(clicked_id)(function () {
        eel.displayWebCommand()();
    });
}

// 3. Contact Delete - FIXED WITH CALLBACK
function ContactDeleteID(clicked_id) {
    eel.deletePhoneBookCommand(clicked_id)(function () {
        eel.displayPhoneBookCommand()();
    });
}