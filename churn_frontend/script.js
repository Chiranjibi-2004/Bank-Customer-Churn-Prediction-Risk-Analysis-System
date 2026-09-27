/*
=================================================
    CUSTOMER CHURN PREDICTION FRONTEND
=================================================

    Backend:
    http://127.0.0.1:8000

    Endpoint:
    POST /predict

    Expected response:

    {
        "predicted_result": 1,
        "churn_probability": 72.45,
        "stay_probability": 27.55
    }

=================================================
*/


/* =============================================
   API URL
============================================= */

const API_URL =
    "http://127.0.0.1:8000/predict";



/* =============================================
   GET HTML ELEMENTS
============================================= */

const form =
    document.getElementById(
        "predictionForm"
    );


const predictButton =
    document.getElementById(
        "predictButton"
    );


const resetButton =
    document.getElementById(
        "resetButton"
    );


const buttonText =
    document.getElementById(
        "buttonText"
    );


const errorMessage =
    document.getElementById(
        "errorMessage"
    );


const resultCard =
    document.getElementById(
        "resultCard"
    );


const initialResult =
    document.getElementById(
        "initialResult"
    );


const resultDetails =
    document.getElementById(
        "resultDetails"
    );


const riskPercentage =
    document.getElementById(
        "riskPercentage"
    );


const riskTitle =
    document.getElementById(
        "riskTitle"
    );


const riskBadge =
    document.getElementById(
        "riskBadge"
    );


const riskCircle =
    document.getElementById(
        "riskCircle"
    );


const churnPercentage =
    document.getElementById(
        "churnPercentage"
    );


const stayPercentage =
    document.getElementById(
        "stayPercentage"
    );


const churnBar =
    document.getElementById(
        "churnBar"
    );


const stayBar =
    document.getElementById(
        "stayBar"
    );


const analysisText =
    document.getElementById(
        "analysisText"
    );


const predictionValue =
    document.getElementById(
        "predictionValue"
    );


const metaChurn =
    document.getElementById(
        "metaChurn"
    );


const metaStay =
    document.getElementById(
        "metaStay"
    );



/* =============================================
   GET FORM VALUE
============================================= */

function getValue(id) {

    return document
        .getElementById(id)
        .value;

}



/* =============================================
   COLLECT CUSTOMER DATA
============================================= */

function getCustomerData() {

    return {

        creditscore:
            Number(
                getValue("creditscore")
            ),

        age:
            Number(
                getValue("age")
            ),

        tenure:
            Number(
                getValue("tenure")
            ),

        balance:
            Number(
                getValue("balance")
            ),

        numofproducts:
            Number(
                getValue("numofproducts")
            ),

        hascrcard:
            Number(
                getValue("hascrcard")
            ),

        isactivemember:
            Number(
                getValue("isactivemember")
            ),

        estimatedsalary:
            Number(
                getValue("estimatedsalary")
            ),

        satisfaction_score:
            Number(
                getValue(
                    "satisfaction_score"
                )
            ),

        card_type:
            getValue("card_type"),

        point_earned:
            Number(
                getValue("point_earned")
            ),

        gender:
            getValue("gender"),

        geography:
            getValue("geography")
    };

}



/* =============================================
   SHOW LOADING
============================================= */

function setLoading(isLoading) {

    if (isLoading) {

        predictButton.disabled = true;

        predictButton.classList.add(
            "loading"
        );

    } else {

        predictButton.disabled = false;

        predictButton.classList.remove(
            "loading"
        );

    }

}



/* =============================================
   ERROR HANDLING
============================================= */

function showError(message) {

    errorMessage.textContent =
        message;

    errorMessage.style.display =
        "block";

}


function hideError() {

    errorMessage.textContent = "";

    errorMessage.style.display =
        "none";

}



/* =============================================
   DISPLAY PREDICTION
============================================= */

function displayPrediction(
    prediction,
    churnProbability,
    stayProbability
) {


    /* Convert to numbers */

    const predicted =
        Number(prediction);


    const churn =
        Number(churnProbability);


    const stay =
        Number(stayProbability);



    /* =========================================
       VALIDATE RESPONSE
    ========================================== */

    if (
        !Number.isFinite(churn) ||
        !Number.isFinite(stay)
    ) {

        throw new Error(
            "Invalid probability returned by API."
        );

    }



    /* =========================================
       SHOW RESULT
    ========================================== */

    initialResult.style.display =
        "none";


    resultDetails.classList.remove(
        "hidden"
    );


    /* Remove previous state */

    resultCard.classList.remove(
        "high-risk",
        "low-risk"
    );



    /* =========================================
       RISK SCORE
    ========================================== */

    /*
        If prediction = 1:
        Show churn probability.

        If prediction = 0:
        Show stay probability.

        This matches the logic from
        your Streamlit application.
    */

    let riskScore;


    if (predicted === 1) {

        riskScore = churn;

    } else {

        riskScore = stay;

    }



    riskPercentage.textContent =
        `${riskScore.toFixed(1)}%`;



    /* =========================================
       HIGH CHURN RISK
    ========================================== */

    if (predicted === 1) {

        resultCard.classList.add(
            "high-risk"
        );


        riskTitle.textContent =
            "High Churn Risk";


        riskBadge.textContent =
            "⚠ Customer likely to leave";


        predictionValue.textContent =
            "Churn";


        analysisText.textContent =
            `The model estimates a ${churn.toFixed(2)}% `
            + `probability that this customer may leave `
            + `the bank. This customer may require `
            + `proactive retention attention.`;

    }


    /* =========================================
       LOW CHURN RISK
    ========================================== */

    else {

        resultCard.classList.add(
            "low-risk"
        );


        riskTitle.textContent =
            "Low Churn Risk";


        riskBadge.textContent =
            "✓ Customer likely to stay";


        predictionValue.textContent =
            "Stay";


        analysisText.textContent =
            `The model estimates a ${stay.toFixed(2)}% `
            + `probability that this customer will stay `
            + `with the bank. The customer currently `
            + `shows a lower churn risk.`;

    }



    /* =========================================
       PROBABILITY TEXT
    ========================================== */

    churnPercentage.textContent =
        `${churn.toFixed(2)}%`;


    stayPercentage.textContent =
        `${stay.toFixed(2)}%`;


    metaChurn.textContent =
        `${churn.toFixed(2)}%`;


    metaStay.textContent =
        `${stay.toFixed(2)}%`;



    /* =========================================
       RESET PROGRESS BARS
    ========================================== */

    churnBar.style.width =
        "0%";


    stayBar.style.width =
        "0%";



    /* =========================================
       ANIMATE PROGRESS BARS
    ========================================== */

    setTimeout(function() {

        churnBar.style.width =
            `${Math.min(churn, 100)}%`;


        stayBar.style.width =
            `${Math.min(stay, 100)}%`;

    }, 100);



    /* =========================================
       CIRCULAR RISK SCORE
    ========================================== */

    const circumference =
        2 * Math.PI * 50;


    const offset =
        circumference -
        (
            riskScore / 100
        ) * circumference;


    /*
        Reset first so animation
        happens every prediction.
    */

    riskCircle.style.strokeDashoffset =
        circumference;


    setTimeout(function() {

        riskCircle.style.strokeDashoffset =
            offset;

    }, 100);

}



/* =============================================
   FORM SUBMISSION
============================================= */

form.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        /* Hide old errors */

        hideError();


        /* Collect data */

        const customerData =
            getCustomerData();


        console.log(
            "Customer data:",
            customerData
        );


        /* Loading */

        setLoading(true);


        try {


            /* =================================
               SEND REQUEST
            ================================== */

            const response =
                await fetch(
                    API_URL,
                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify(
                                customerData
                            )

                    }
                );



            /* =================================
               HTTP ERROR
            ================================== */

            if (!response.ok) {

                let errorData = null;


                try {

                    errorData =
                        await response.json();

                } catch {

                    errorData = null;

                }


                let message =
                    `API request failed `
                    + `with status ${response.status}.`;



                /*
                    FastAPI validation
                    error handling
                */

                if (
                    errorData &&
                    errorData.detail
                ) {

                    if (
                        Array.isArray(
                            errorData.detail
                        )
                    ) {

                        message =
                            errorData.detail
                                .map(
                                    error =>
                                        error.msg
                                )
                                .join(
                                    ", "
                                );

                    } else {

                        message =
                            errorData.detail;

                    }

                }


                throw new Error(
                    message
                );

            }



            /* =================================
               READ RESPONSE
            ================================== */

            const result =
                await response.json();


            console.log(
                "Prediction response:",
                result
            );



            /* =================================
               DISPLAY RESULT
            ================================== */

            displayPrediction(

                result.predicted_result,

                result.churn_probability,

                result.stay_probability

            );


        }


        /* =====================================
           CONNECTION / OTHER ERROR
        ====================================== */

        catch (error) {

            console.error(
                "Prediction error:",
                error
            );


            if (
                error instanceof
                TypeError
            ) {

                showError(
                    "Unable to connect to the FastAPI server. "
                    +
                    "Make sure uvicorn is running at "
                    +
                    "http://127.0.0.1:8000"
                );

            } else {

                showError(
                    error.message
                );

            }

        }


        /* =====================================
           STOP LOADING
        ====================================== */

        finally {

            setLoading(false);

        }

    }
);



/* =============================================
   RESET FORM
============================================= */

resetButton.addEventListener(
    "click",
    function() {


        /* Reset HTML form */

        form.reset();



        /* =====================================
           DEFAULT VALUES
        ====================================== */

        document.getElementById(
            "creditscore"
        ).value = 650;


        document.getElementById(
            "age"
        ).value = 35;


        document.getElementById(
            "tenure"
        ).value = 5;


        document.getElementById(
            "balance"
        ).value = 50000;


        document.getElementById(
            "numofproducts"
        ).value = 2;


        document.getElementById(
            "hascrcard"
        ).value = 1;


        document.getElementById(
            "isactivemember"
        ).value = 1;


        document.getElementById(
            "estimatedsalary"
        ).value = 50000;


        document.getElementById(
            "satisfaction_score"
        ).value = 3;


        document.getElementById(
            "card_type"
        ).value = "SILVER";


        document.getElementById(
            "point_earned"
        ).value = 500;


        document.getElementById(
            "gender"
        ).value = "Male";


        document.getElementById(
            "geography"
        ).value = "France";



        /* =====================================
           RESET ERROR
        ====================================== */

        hideError();



        /* =====================================
           RESET RESULT CARD
        ====================================== */

        resultCard.classList.remove(
            "high-risk",
            "low-risk"
        );


        resultDetails.classList.add(
            "hidden"
        );


        initialResult.style.display =
            "flex";



        /* =====================================
           RESET PROGRESS BARS
        ====================================== */

        churnBar.style.width =
            "0%";


        stayBar.style.width =
            "0%";



        /* =====================================
           RESET CIRCULAR SCORE
        ====================================== */

        riskCircle.style.strokeDashoffset =
            "314.159";


        /* Reset text */

        riskPercentage.textContent =
            "0%";


        riskTitle.textContent =
            "Low Risk";


        riskBadge.textContent =
            "✓ Customer likely to stay";


        predictionValue.textContent =
            "—";


        churnPercentage.textContent =
            "0.00%";


        stayPercentage.textContent =
            "0.00%";


        metaChurn.textContent =
            "—";


        metaStay.textContent =
            "—";


        analysisText.textContent =
            "Model interpretation will appear here.";

    }
);