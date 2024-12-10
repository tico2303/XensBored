import { Component, Input } from '@angular/core';
import { AppService } from '../app.service';
import { Suggestion,SuggestionResults } from '../models/suggestions';
@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrl: './results.component.scss'
})
export class ResultsComponent {
  suggestion:Suggestion = new SuggestionResults();
  //@Input() suggestion:Suggestion = new SuggestionResults(); 
  constructor(public appService:AppService){
    console.log("results constructur")
  }
  ngOnInit() {
    console.log("results ngOnInit ")
    this.appService.currentSuggestion.subscribe((newSuggestion)=>{
      this.suggestion = newSuggestion
      this.appService.loading.next(false)  
    })
  }
}
