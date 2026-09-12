const askButton = document.getElementById("askButton");
const questionBox = document.getElementById("question");

const loading = document.getElementById("loading");
const result = document.getElementById("result");

const statusBox = document.getElementById("status");
const answerBox = document.getElementById("answer");
const sourcesBox = document.getElementById("sources");

const suggestions =
    document.querySelectorAll(".suggestion");


// ==========================================
// ASK BUTTON
// ==========================================

askButton.addEventListener(
    "click",
    askQuestion
);


// ==========================================
// ENTER SHORTCUT
// ==========================================

questionBox.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Enter"
            && !event.shiftKey
        ) {
            event.preventDefault();

            askQuestion();
        }

    }
);


// ==========================================
// SUGGESTION BUTTONS
// ==========================================

suggestions.forEach(
    function (button) {

        button.addEventListener(
            "click",
            function () {

                questionBox.value =
                    button.dataset.question;

                questionBox.focus();

            }
        );

    }
);


// ==========================================
// ASK QUESTION
// ==========================================

async function askQuestion() {

    const question =
        questionBox.value.trim();


    if (!question) {

        questionBox.focus();

        return;
    }


    // --------------------------------------
    // Loading state
    // --------------------------------------

    loading.classList.remove(
        "hidden"
    );

    result.classList.add(
        "hidden"
    );

    askButton.disabled = true;


    const buttonText =
        askButton.querySelector(
            ".button-text"
        );

    buttonText.textContent =
        "Searching...";


    try {

        const response =
            await fetch(
                "/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                "API request failed"
            );
        }


        const data =
            await response.json();


        // ----------------------------------
        // Status
        // ----------------------------------

        statusBox.textContent =
            data.status;


        statusBox.className =
            "status-badge";


        if (
            data.status ===
            "ANSWERED"
        ) {

            statusBox.classList.add(
                "answered"
            );

        } else {

            statusBox.classList.add(
                "not-covered"
            );

        }


        // ----------------------------------
        // Answer
        // ----------------------------------

        answerBox.textContent =
            data.answer ||
            "No answer available.";


        // ----------------------------------
        // Sources
        // ----------------------------------

        sourcesBox.innerHTML = "";


        if (
            data.sources &&
            data.sources.length > 0
        ) {

            data.sources.forEach(
                function (source) {

                    const card =
                        document.createElement(
                            "div"
                        );

                    card.className =
                        "source-card";


                    const type =
                        source.type ||
                        "document";


                    let label = "PDF";


                    if (
                        type ===
                        "handwritten"
                    ) {
                        label = "OCR";
                    }

                    else if (
                        type ===
                        "pptx"
                    ) {
                        label = "PPT";
                    }


                    const pageLabel =
                        source.page !== null &&
                        source.page !== undefined
                            ? `Page ${source.page}`
                            : "OCR document";


                    card.innerHTML = `

                        <div class="source-left">

                            <div class="source-icon">
                                ${label}
                            </div>

                            <div>

                                <div class="source-name">
                                    ${escapeHTML(
                                        source.source ||
                                        "Unknown source"
                                    )}
                                </div>

                                <div class="source-meta">
                                    <span>${pageLabel}</span>
                                    <span>${type}</span>
                                </div>

                            </div>

                        </div>


                        <div class="score">
                            ${Number(
                                source.score || 0
                            ).toFixed(4)}
                        </div>

                    `;


                    sourcesBox.appendChild(
                        card
                    );

                }
            );

        } else {

            sourcesBox.innerHTML = `

                <div class="source-card">

                    <div class="source-left">

                        <div class="source-icon">
                            —
                        </div>

                        <div>

                            <div class="source-name">
                                No supporting sources
                            </div>

                            <div class="source-meta">
                                <span>The material does not provide supporting evidence.</span>
                            </div>

                        </div>

                    </div>

                </div>

            `;

        }


        // ----------------------------------
        // Show result
        // ----------------------------------

        result.classList.remove(
            "hidden"
        );


        // Smooth scroll
        result.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });


    } catch (error) {

        console.error(error);


        answerBox.textContent =
            "Could not connect to StudyVault AI. " +
            "Please make sure the FastAPI server is running.";


        statusBox.textContent =
            "ERROR";


        statusBox.className =
            "status-badge not-covered";


        sourcesBox.innerHTML = "";


        result.classList.remove(
            "hidden"
        );

    } finally {

        loading.classList.add(
            "hidden"
        );

        askButton.disabled = false;

        buttonText.textContent =
            "Ask StudyVault";

    }

}


// ==========================================
// HTML ESCAPE
// ==========================================

function escapeHTML(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}