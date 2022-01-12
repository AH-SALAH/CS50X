// scope trivia object
const trivia = {
    // cache vars
    section1: () => document.querySelector(".section-1"),
    section2: () => document.querySelector(".section-2"),
    // create static Questions data for multiple and free Q
    multiQ: [
        {
            q1: "What is the Capital of Palestine?",
            answers: [
                { "Cairo": false },
                { "Istanbul": false },
                { "Quds": true },
                { "Amman": false }
            ]
        },
        {
            q2: "To avoid get infected by covid-19 as possible as i can, I should wear?",
            answers: [
                { "Apple watch": false },
                { "medical level mask": true },
                { "Ray-Ban sunglasses": false },
                { "VR Headset": false },
                { "Wrist Band Bracelet": false }
            ]
        }
    ],
    formAnswer: "...........",
    freeQ: function () { return [`Rabaa Massacre occured in Egypt after a military coup by <span style="color: dodgerblue;text-decoration: underline;">${this.formAnswer}</span>`, "sisi"] },
    //shorten createEl
    createElement: el => document.createElement(el),
    // create section 1
    createSection1: function () {
        // if there is no section 1 el return;
        if (!this.section1()) return;
        // create doc fragment to insert once in the dom [better performance]
        let vDom = document.createDocumentFragment();
        // loop through multi questions and create dom data 
        // create main container and put elements inside and append to fragment dom
        // then append fragment dom into real dom obj once
        this.multiQ.map((item, i) => {
            let h3 = this.createElement("h3"),
                container = this.createElement("div"),
                optContainer = this.createElement("div"),
                span = this.createElement("span");

            container.classList.add("q-container", "q" + (i + 1));
            optContainer.classList.add("options-container");
            span.classList.add("result");
            span.innerHTML = "Answer";

            h3.innerHTML = item['q' + (i + 1)];
            container.append(h3, span);

            for (let a of item.answers) {
                let div = this.createElement("div");

                div.classList.add("options-wrapper");

                for (let key in a) {
                    if (a.hasOwnProperty(key)) {
                        let btn = this.createElement("button");

                        btn.classList.add("opt-btn");
                        btn.innerHTML = key;
                        // handle btn click
                        this.handleClick(btn, a[key], container);
                        div.append(btn);
                    }
                }
                optContainer.append(div);
            }
            // append all into the main container
            container.append(optContainer);
            // then into virtual dom [fragment]
            vDom.append(container);
        });
        // append fragment into section 1 [of the real dom]
        this.section1().append(vDom);
    },
    // handle section 1 btns click
    handleClick: function (btn, val, container) {
        if (!btn || !container) return;

        btn.addEventListener('click', function () {
            if (this.classList.contains("btn-correct") || this.classList.contains("btn-incorrect")) return;

            // let optWrp = this.parentElement.parentElement?.querySelectorAll('.result');
            let span = container.querySelector('.result');
            if (!span) span = document.createElement("span");
            container.querySelectorAll('.opt-btn').forEach(element => {
                // element.previousSibling?.classList.remove("btn-correct", "btn-incorrect");
                element.classList.remove("btn-correct", "btn-incorrect");
                // element.remove();
            });
            span.innerHTML = val ? "Correct!" : "Incorrect";
            if (val) {
                span.classList.add("correct");
                span.classList.remove("incorrect");
                this.classList.remove("btn-incorrect");
                this.classList.add("btn-correct");
            }
            else {
                span.classList.add("incorrect");
                span.classList.remove("correct");
                this.classList.remove("btn-correct");
                this.classList.add("btn-incorrect");
            }

            // this.parentElement.append(span);
        });
    },
    // create section 2 like section 1 but with different data structure
    createSection2: function () {
        if (!this.section2) return;

        let vDom = document.createDocumentFragment();
        let item = this.freeQ();
        // this.freeQ.map((item, i) => {
        let h3 = this.createElement("h3"),
            container = this.createElement("div"),
            optContainer = this.createElement("div"),
            frm = this.createElement("form"),
            txtInput = this.createElement("input"),
            submitBtn = this.createElement("input"),
            span = this.createElement("span");

        container.classList.add("q-container", "q2");
        optContainer.classList.add("options-container");

        txtInput.setAttribute("type", "text");
        txtInput.setAttribute("name", "q1-input");
        txtInput.setAttribute("placeholder", "evil person name..");
        txtInput.setAttribute("autocomplete", "off");
        submitBtn.setAttribute("type", "submit");
        submitBtn.setAttribute("value", "Submit");
        frm.append(txtInput, submitBtn);

        span.classList.add("result");
        span.innerHTML = "Answer";

        h3.innerHTML = item[0];

        container.append(h3, span, frm);
        // handle input keyup change
        this.handleInputChange(txtInput);
        // handle form submit
        this.handleF2Submit(frm, txtInput, item[1], span);

        vDom.append(container);
        // });

        this.section2().append(vDom);
    },
    // handle input change
    handleInputChange: function (input) {
        if (!input) return;
        self = this;
        input.addEventListener('keyup', function () {
            let ttl = self.section2().querySelector(".q-container.q2 h3"),
                res = self.section2().querySelector(".q-container.q2 .result");
            // if no value, return to default val
            if (!this.value) {
                self.formAnswer = "...........";
                ttl.innerHTML = self.freeQ()[0];
                this.classList.remove("incorrect", "correct");
                res.classList.remove("incorrect", "correct");
                res.innerHTML = "Answer";
                return;
            }
            // change dom q with the new real time written input value
            self.formAnswer = this.value;
            ttl.innerHTML = self.freeQ()[0];
        });
    },
    // handle form submit
    handleF2Submit: function (form, input, correctAnswer, answerEl) {
        if (!form && !input && !answerEl) return;

        form.addEventListener('submit', e => {
            e.preventDefault();
            if (!input.value) return;
            let val = input.value.trim().toLocaleLowerCase();
            let regex = RegExp(correctAnswer, 'gi');
            if (val.search(regex) > -1) {
                answerEl.classList.remove('incorrect');
                answerEl.classList.add('correct');
                answerEl.innerHTML = "Correct!";
                input.classList.add('correct');
                input.classList.remove('incorrect');
            }
            else {
                answerEl.classList.remove('correct');
                answerEl.classList.add('incorrect');
                answerEl.innerHTML = "Incorrect";
                input.classList.add('incorrect');
                input.classList.remove('correct');

            }
        });
        return false;
    },
    // initialize functions
    init: function () {
        this.createSection1();
        this.createSection2();
    }
}
// init after dom loaded to just affirm
window.addEventListener('DOMContentLoaded', () => {
    trivia.init();
});