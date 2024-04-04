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
            isROIPredictor2Showing: false,
            isROICalculatorShowing: false,
            selectedCrop: "",
            cropIsSelected: false,
            roiData: [],
            contingencyPercent: "",
            grossIncome: "",
            contingencyCost: "",
            totalCost: 0,
            netIncome: 0,
            roi: 1,
            isModelTrained: false,
            trainModelUrl: "",
            trainModelUrl2: "",
            isLoading: false,
            accuracy: '',
            recall: '',
            precision: '',
            f1Score: '',
            roi2CropBg: '',
            linearRegressionScores: {},
          }
        },
        watch: {
          roiData: {
            handler(newValue, oldValue) {
              this.computeForPHPamt();
            },
            deep: true,
          },
          isROIPredictor2Showing: {
            handler(newValue, oldValue) {
              if(this.isROIPredictor2Showing){
                this.initializeTrainBtn2();
                this.listenToRoi2CropInput();
              }
            }            
          }
        },
        async mounted(){
          this.resetDataValues();
          this.trainModelUrl = document.getElementById('train-classifier-url') ? document.getElementById('train-classifier-url').value : "";
          this.trainModelUrl2 = document.getElementById('train-classifier-2-url') ? document.getElementById('train-classifier-2-url').value : "";
          await this.initializeTrainBtn();

          this.checkIfClassifier2IsUsed();
        },
        methods: {
          initializeTrainBtn2(){
            let vueApp = this;
            
            $(document).ready(function() {
              $('#train-btn2').on('click', function() {  
                vueApp.resetDataValues();
                vueApp.isLoading = true;
                $.ajax({
                  url: vueApp.trainModelUrl2,
                  type: 'GET',
                  success: function(response) {
                    vueApp.isModelTrained = true;
                    
                    setTimeout(function() {
                      alert('Notice: Model Successfully Trained');
                      vueApp.isLoading = false;
                      vueApp.linearRegressionScores = response.model_output
                    }, 2000);
                  },
                  error: function(error) {
                    alert('Notice: Model Training failed');
                    vueApp.isLoading = false;
                  }
                });
              });
            });
          },
          initializeTrainBtn(){

            let vueApp = this;
            $(document).ready(function() {
              $('#train-btn').on('click', function() {
                vueApp.isLoading = true;
                $.ajax({
                  url: vueApp.trainModelUrl,
                  type: 'GET',
                  success: function(response) {
                    vueApp.isModelTrained = true;
                    
                    setTimeout(function() {
                      alert('Notice: Model Successfully Trained');
                      vueApp.isLoading = false;
                      vueApp.accuracy = response.model_output.accuracy
                      vueApp.precision = response.model_output.precision
                      vueApp.recall = response.model_output.recall
                      vueApp.f1Score = response.model_output.f1_score
                      // vueApp.accuracy = response.model_output.accuracy
                    }, 2000);
                  },
                  error: function(error) {
                    alert('Notice: Model Training failed');
                    vueApp.isLoading = false;
                  }
                });
              });
            });
          },
          checkIfClassifier2IsUsed(){
            let divContent = $("#classifier-2-output").text();
          
            if(divContent){
              console.log(divContent);
              this.selectROIOption('predictor2');
            }

          },
          switchCarouselImg(action){
            if(action == 'next'){
              this.carouselIndex = this.carouselIndex === 2 ? 0 : this.carouselIndex + 1;
            }else if (action == 'prev'){
              this.carouselIndex = this.carouselIndex === 0 ? 2 : this.carouselIndex - 1;
            }
          },
          selectROIOption(ROIOption){
            this.isROIPredictorShowing = true ? ROIOption === 'predictor' : false;
            this.isROIPredictor2Showing = true ? ROIOption === 'predictor2' : false;
            this.isROICalculatorShowing = true ? ROIOption === 'calculator' : false;
            this.resetDataValues();
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
          listenToRoi2CropInput(){
            let vueApp = this;
            $(document).ready(function() {
              
              const selectedCrop = document.querySelector('.selected-crop-2');
              const crop = selectedCrop?.innerText.trim();
              
              if(!crop){
                return;
              }

              vueApp.roi2CropBg = crop.toLowerCase() + '-bg';
              if(crop == "Sweet Potato"){
                vueApp.roi2CropBg = 'sweet-potato-bg';
              }
              
            });
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
          calculateROIData(){

            if(!this.contingencyPercent){
              alert("Input Contingency Percent Cost (ex. 0.10 for 10%).");
              return;
            }

            if(!this.grossIncome){
              alert("Input Gross Income (ex. 70000).");
              return;
            }

            this.totalCost = 0;

            for(let i = 0; i < this.roiData.length; i++){

              if(this.roiData[i]?.sectionContent.length){
                for(let j = 0; j < this.roiData[i]?.sectionContent.length; j++){
                  
                  this.totalCost = this.totalCost + this.roiData[i].sectionContent[j].amtPHP;
                  
                }
              }
            }

            this.contingencyCost = Number(this.totalCost) * Number(this.contingencyPercent);
            this.totalCost = Number(this.totalCost) + Number(this.contingencyCost);

            this.netIncome = Number(this.grossIncome) - Number(this.totalCost);

            this.roi = Number(this.grossIncome) / Number(this.totalCost);
            this.roi = (this.roi * 100).toFixed(2) + "%"

            this.outputROICalculatedData();
          },
          outputROICalculatedData(){
            
            let message = "The computed ROI for the given data:\n";
          
            alert(
              message + 
              "Contingency Cost: " + this.contingencyCost + "\n" +
              "Total Cost: " + this.totalCost + "\n" +
              "Gross Income: " + this.grossIncome + "\n" + 
              "Net Income: " + this.netIncome + "\n" + 
              "ROI(%): " + this.roi
            );

          },
          async resetDataValues(){
            // await this.initializeTrainBtn();
            this.selectedCrop = "";
            this.cropIsSelected = false;
            this.roiData = [];
            this.contingencyPercent = "";
            this.grossIncome = "";
            this.contingencyCost = "";
            this.totalCost = 0;
            this.netIncome = 0;
            this.roi = 1;
            this.isModelTrained = false;
            this.accuracy = '';
            this.recall = '';
            this.precision = '';
            this.f1Score = '';
          },
        }
      }).mount("#binhi-main-container");
    }
  }
}

export { MainApp }; 