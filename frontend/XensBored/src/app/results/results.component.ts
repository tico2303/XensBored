import { Component, Input } from '@angular/core';
import { AppService } from '../app.service';
import { Suggestion,SuggestionResults } from '../models/suggestions';
import { ToastrService } from 'ngx-toastr';
@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrl: './results.component.scss'
})
export class ResultsComponent {
  suggestion:Suggestion = new SuggestionResults();
  hasResults:boolean = false;
  //@Input() suggestion:Suggestion = new SuggestionResults(); 
  constructor(public appService:AppService, public toastr:ToastrService) {   
    console.log("results constructur")
  }
  ngOnInit() {
    this.hasResults = false;
    this.appService.currentSuggestion.subscribe((newSuggestion)=>{
      this.suggestion = newSuggestion
      console.log("hasResults:",this.hasResults)
      if(newSuggestion.status==="error"){
        this.toastr.error(newSuggestion.message)
      }
      if(this.suggestion.suggestions.length>0){
        this.hasResults=true;
      }
      console.log("results ngOnInit newSuggestion",newSuggestion)
      this.appService.loading.next(false)  
    })
  }
}
