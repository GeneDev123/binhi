class MainApp {
  constructor() {}

  async mainApp() {
    
    if(document.getElementById("binhi-main-container")){
      Vue.createApp({
        delimiters: ['[[', ']]'],
        data(){
          return {
            carouselIndex: 0,
            trainClassifierUrl: "", 

            accuracy: '',
            precision: '',
            recall: '',
            confusionMat: '',
            f1Score: '',
          }
        },
        components: {
  
        },
        async created(){

        },
        mounted(){
          
          this.trainClassifierUrl = document.getElementById('train-classifier-var').value;

          const thisVue = this;
          $(document).ready(function() {
            $('#train-classifier-btn').click(function() {
              $.ajax({
                url: thisVue.trainClassifierUrl,
                type: "GET",
                success: function(response) {
                  thisVue.outputClassifierTraining(response.data);
                },
                error: function(xhr) {
                  console.log(xhr.status);
                }
              });
            });
          });

        },
        methods: {
          switchCarouselImg(action){
            if(action == 'next'){
              this.carouselIndex = this.carouselIndex === 2 ? 0 : this.carouselIndex + 1;
            }else if (action == 'prev'){
              this.carouselIndex = this.carouselIndex === 0 ? 2 : this.carouselIndex - 1;
            }
          },
          outputClassifierTraining(data){
            this.accuracy = data.accuracy;
            this.precision = data.precision;
            this.recall = data.recall;
            this.f1Score = data.f1_score;
            this.confusionMat = data.confusion_mat;
          }
        }
      }).mount("#binhi-main-container");
    }
  }
}

export { MainApp }; 