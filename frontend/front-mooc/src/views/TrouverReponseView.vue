<template>
    <BarreDeNavigation />
    <main>
        <!-- Select pour choisir cours -->
        <h2>Question/Réponse</h2>
        <div class="mb-3 question-form2">
            <label class="form-label fw-bold">Choisissez le cours concerné :</label>
            <select class="form-select" v-model="selectedCourse">
                <option value=''></option>
                <option
                  v-for="(course, index) in courses"
                  :key="index"
                  :value="course.course_id">
                    {{ course.course_id }}
                </option>
            </select>
        </div>

        <!-- Input pour poser une question -->
        <div class="mb-3 question-form" v-if="selectedCourse">
            <label class="form-label fw-bold">Posez votre question :</label>
            <div>
                <input type="text" class="form-control question-data" placeholder="">

            </div>

        </div>
        <button type="button" class="btn btn-dark valider" :onclick=ValiderQuestion >Valider</button>
        <!-- Liste des résultats -->
        <section v-if="question" class="section-resultats">
            <div class="">
                <h4 class="fw-bold">
                    Fils de discussions recommandés : <br>
                    <span class="discussion-question">"{{ question }}"</span>
                </h4>
            </div>
            <ResultatsFils :threads="filteredThreads" />
        </section>
    </main>
</template>


<script >

import apiClient from "@/api/axios";
import BarreDeNavigation from "../components/BarreDeNavigation.vue";
import ResultatsFils from "../components/ResultatsFils.vue";

//import axios from "axios";
// import courses from "../data/courses.json";
// import threads from "../data/threads.json";

export default {
    components: {
        BarreDeNavigation,
        ResultatsFils
    },
    data() {
        return {
            courses: [],
            threads: {},
            selectedCourse: null,
            question: "",
        };
    },
    methods: {
        getCourses(){
            console.log('Not', localStorage.getItem('token'))
            apiClient.get("/api/courses")
            .then( response =>{
                this.courses = response.data;
                // this.selectedCourse = this.courses[0].course_id || this.courses[0].id;
                this.selectedCourse = "";
                console.log(this.selectedCourse);

            })
        },
        getThreads(){
            apiClient.get("/api/courses/" + this.selectedCourse)
            .then( response =>{
                this.threads = response.data;

            })
        },

        ValiderQuestion(){
            console.log("Question validée");
            let questionData = document.querySelector(".question-data");
            questionData = questionData.value;
            this.question = questionData;
            console.log(this.question);
            this.getThreads();
            console.log(this.selectedCourse)
            let data  = {
              course_id : this.selectedCourse,
              prompt    : this.question
            }
            apiClient.post("/api/rag", data)
            .then(response => {
            console.log(response.data)
            this.threads = response.data
            })

        }
    },
    mounted() {
        this.getCourses();
        // this.threads = threads;

    },
    computed: {
        filteredThreads() {
            return this.threads || [];
        }



    }
};
</script>



<style scoped>
main {
    padding: 50px;
    display: flex;
    flex-direction: column;
    align-items: center;
    color: rgb(21, 31, 101)!important;
}

.question-form,
.question-form2 {
    width: 500px;
}

.question-form div {
    display: flex;
    gap: 10px;
}
.valider {
    margin-top: 20px;
    width: 200px;
}
section {
    margin-top: 50px;
}

.section-resultats {
    width: 1000px;
}

.discussion-header {
    background-color: #f4f8fe;
    border-radius: 14px;
    box-shadow: 0 2px 8px 0 rgba(100, 100, 130, 0.059);
    padding: 32px 32px 20px 32px;
    margin-bottom: 30px;
    text-align: left;
    border: 1px solid #f0f2f7;
}

.discussion-header h3 {
    font-size: 1.45rem;
    font-weight: 600;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.discussion-course {
    font-size: 1rem;
    color: #246ef4;
    font-weight: 400;
    margin-left: 8px;
}

.discussion-question {
    font-size: 1.13rem;
    color: #444;
    margin: 0;
}

.discussion-question span {
    color: #246ef4;
    font-style: italic;
    font-weight: 500;
    font-size: 16px;
}


</style>
