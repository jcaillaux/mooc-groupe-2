<template>
    <BarreDeNavigation />
    <main>
        <!-- Select pour choisir cours -->
        <div class="mb-3 question-form2">
            <label class="form-label">Choisissez le cours concerné :</label>
            <select class="form-select" v-model="selectedCourse">
                <option 
                  v-for="(course, index) in courses" 
                  :key="index" 
                  :value="course.course_id">
                    {{ course.course_id }}
                </option>
            </select>
        </div>

        <!-- Input pour poser une question -->
        <div class="mb-3 question-form">
            <label class="form-label">Posez votre question :</label>
            <div>
                <input type="text" class="form-control" placeholder="">
                <button type="button" class="btn btn-dark">Valider</button>
            </div>
        </div>

        <!-- Liste des résultats -->
        <section>
            <h3>Fils de discussions</h3>
            <ResultatsFils :threads="filteredThreads" />
        </section>
    </main>
</template>

<script scoped>
import BarreDeNavigation from "../components/BarreDeNavigation.vue";
import ResultatsFils from "../components/ResultatsFils.vue";

import axios from "axios";
// import courses from "../data/courses.json";
import threads from "../data/threads.json";

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
        };
    },
    methods: {
        getCourses(){
            axios.get("http://127.0.0.1:5000/api/courses")
            .then( response =>{
                this.courses = response.data;
                this.selectedCourse = this.courses[0].course_id || this.courses[0].id;
                alert(this.selectedCourse);
                
            })
        }
    },
    mounted() {
        this.getCourses();
        this.threads = threads;
        
    },
    computed: {
        filteredThreads() {
            return this.threads[this.selectedCourse] || [];
        }
        
    }
};
</script>



<style scoped>
/* Input pour poser une question */
        main{
            padding: 50px;
        }
        .question-form{
            max-width: 500px;
        }
        .question-form2{
            max-width: 416px;
        }
        .question-form div{
            display: flex;
            gap: 10px;
        }
        section{
            margin-top: 50px;
        }
</style>