async function loadStatistics() {

    try {

        const response = await fetch("/api/statistics");

        const data = await response.json();

        document.getElementById("total").textContent = data.total;

        document.getElementById("errors").textContent = data.errors;

        document.getElementById("warnings").textContent = data.warnings;

        document.getElementById("critical").textContent = data.critical;

    }

    catch (error) {

        console.error("Error loading statistics:", error);

    }
}


async function loadLogs() {

    try {

        const response = await fetch("/api/logs");

        const logs = await response.json();

        const table = document.getElementById("logTable");

        const alerts = document.getElementById("alerts");

        table.innerHTML = "";

        alerts.innerHTML = "";


        logs.forEach(log => {

            const row = document.createElement("tr");


            row.innerHTML = `

                <td>${log.timestamp}</td>

                <td class="${log.level.toLowerCase()}">
                    ${log.level}
                </td>

                <td>${log.message}</td>

                <td>
                    ${log.failure ? "YES" : "NO"}
                </td>

            `;


            table.appendChild(row);


            if (log.failure) {

                const alert = document.createElement("div");

                alert.className = "alert";


                alert.innerHTML = `

                    <strong>${log.level} ALERT</strong>

                    <br>

                    ${log.message}

                    <br>

                    <small>${log.timestamp}</small>

                `;


                alerts.appendChild(alert);

            }

        });

    }

    catch (error) {

        console.error("Error loading logs:", error);

    }
}


/* -----------------------------------------
   Add New Log
----------------------------------------- */

async function submitLog() {

    const input = document.getElementById("newLog");

    const message = input.value.trim();


    if (!message) {

        alert("Please enter a log message.");

        return;

    }


    try {

        const response = await fetch("/api/logs", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        const data = await response.json();


        if (!response.ok) {

            alert(data.error);

            return;

        }


        input.value = "";


        alert(
            "Log analyzed successfully!\n\n" +
            "Severity: " + data.level + "\n" +
            "Failure: " + (data.failure ? "YES" : "NO")
        );


        refreshDashboard();

    }

    catch (error) {

        console.error("Error submitting log:", error);

        alert("Could not submit the log.");

    }
}


/* -----------------------------------------
   Refresh Dashboard
----------------------------------------- */

function refreshDashboard() {

    loadStatistics();

    loadLogs();

}


/* -----------------------------------------
   Load Dashboard
----------------------------------------- */

refreshDashboard();