import { MainApp } from './modules/Main-App.js'
console.log(1);
(async function($) {
  console.log(2);
  let mainApp = new MainApp()
  let app = await mainApp.mainApp()
  
})(jQuery);