class MainApp {
  constructor() {}

  async mainApp() {
    
    if(document.getElementById("binhi-main-container")){
      Vue.createApp({
        delimiters: ['[[', ']]'],
        data(){
          return {
            carouselIndex: 0,
            webPage: "",
            dataset: {}, 
          }
        },
        components: {
  
        },
        async created(){

        },
        mounted(){
          console.log(this.message);
        },
        methods: {
          switchCarouselImg(action){
            if(action == 'next'){
              this.carouselIndex = this.carouselIndex === 2 ? 0 : this.carouselIndex + 1;
            }else if (action == 'prev'){
              this.carouselIndex = this.carouselIndex === 0 ? 2 : this.carouselIndex - 1;
            }
          },
        }
      }).mount("#binhi-main-container");
    }
  }
}

export { MainApp }; 