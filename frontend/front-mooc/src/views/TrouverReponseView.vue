<template>
    <BarreDeNavigation />
    <main>
        <!-- Select pour choisir cours -->
        <div class="mb-3 question-form2">
            <label class="form-label">Choisissez le cours concerné :</label>
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
            <label class="form-label">Posez votre question :</label>
            <div>
                <input type="text" class="form-control question-data" placeholder="">
                <button type="button" class="btn btn-dark" :onclick=ValiderQuestion >Valider</button>
            </div>
        </div>

        <!-- Liste des résultats -->
        <section v-if="question" class="section-resultats">
            <h3>Fils de discussions recomendés pour :  "{{ question }}""</h3>
            <ResultatsFils :threads="filteredThreads" />
        </section>
    </main>
</template>

<script scoped>

import BarreDeNavigation from "../components/BarreDeNavigation.vue";
import ResultatsFils from "../components/ResultatsFils.vue";

import axios from "axios";
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
            axios.get("http://127.0.0.1:5000/api/courses")
            .then( response =>{
                this.courses = response.data;
                // this.selectedCourse = this.courses[0].course_id || this.courses[0].id;
                this.selectedCourse = "";
                console.log(this.selectedCourse);
                
            })
        },
        getThreads(){
            axios.get("http://127.0.0.1:5000/api/threads/" + this.selectedCourse)
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
/* Input pour poser une question */
        main{
            padding: 50px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .question-form{
            width: 500px;
        }
        .question-form2{
            width: 500px;
            
        }
        .question-form div{
            display: flex;
            gap: 10px;
        }
        section{
            margin-top: 50px;
        }
        .section-resultats{
            width: 1000px;
        }
</style>