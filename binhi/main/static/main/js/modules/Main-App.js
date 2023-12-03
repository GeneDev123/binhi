class MainApp {
  constructor() {}

  async mainApp() {
    
    if(document.getElementById("binhi-main-container")){
      Vue.createApp({
        delimiters: ['[[', ']]'],
        data(){
          return {
            carouselIndex: 0,
            isROIPredictorShowing: true,
            isROICalculatorShowing: false,
            selectedCrop: "",
            cropIsSelected: false,
            roiData: [],

          }
        },
        components: {
  
        },
        async created(){

        },
        watch: {
          roiData: {
            handler(newValue, oldValue) {
              this.computeForPHPamt();
            },
            deep: true,
          },
        },
        mounted(){
        },
        methods: {
          switchCarouselImg(action){
            if(action == 'next'){
              this.carouselIndex = this.carouselIndex === 2 ? 0 : this.carouselIndex + 1;
            }else if (action == 'prev'){
              this.carouselIndex = this.carouselIndex === 0 ? 2 : this.carouselIndex - 1;
            }
          },
          selectROIOption(ROIOption){
            this.isROIPredictorShowing = true ? ROIOption === 'predictor' : false;
            this.isROICalculatorShowing = true ? ROIOption === 'calculator' : false;
          },
          selectCrop(){
            if(!this.selectedCrop) return;

            console.log(this.selectedCrop);
          },
          overrideIfCropIsSelected() {
            if(!this.cropIsSelected){
              this.cropIsSelected = true;
            }else{
              this.refreshCalculator();
            }
          },
          refreshCalculator(args){
            let continueRefresh = window.confirm("Proceeding will delete current data, do you wish to proceed?");
            if(!continueRefresh) return;
            
            if(args?.removeCrop){
              this.selectedCrop = "";
              this.cropIsSelected = false;
            }

            this.roiData = [];
          },
          addSection(){
            this.roiData.push({
              'sectionTitle': '',
              'sectionContent': [],
            })
          },
          addItem(index){
            this.roiData[index].sectionContent.push({
              'item': '',
              'qty': '',
              'unit': '',
              'rate': '',
              'amtPHP': '',
            });
          },
          computeForPHPamt(){
            for(let i = 0; i < this.roiData.length; i++){

              if(this.roiData[i]?.sectionContent.length){
                for(let j = 0; j < this.roiData[i]?.sectionContent.length; j++){
               
                  // Check if data is present and is number
                  if(this.roiData[i].sectionContent[j].qty && this.roiData[i].sectionContent[j].rate){
                    if(!isNaN(this.roiData[i].sectionContent[j].qty) && !isNaN(this.roiData[i].sectionContent[j].rate)){
                      this.roiData[i].sectionContent[j].amtPHP = this.roiData[i].sectionContent[j].qty * this.roiData[i].sectionContent[j].rate
                    }     
                  }
                }
              }
            }
          },
        }
      }).mount("#binhi-main-container");
    }
  }
}

export { MainApp }; 