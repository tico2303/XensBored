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
  //@Input() suggestion:Suggestion = new SuggestionResults(); 
  constructor(public appService:AppService, public toastr:ToastrService) {   
    console.log("results constructur")
  }
  ngOnInit() {
    this.appService.currentSuggestion.subscribe((newSuggestion)=>{
      this.suggestion = newSuggestion
      if(newSuggestion.status==="error"){
        this.toastr.error(newSuggestion.message)
      }
      console.log("results ngOnInit newSuggestion",newSuggestion)
      this.appService.loading.next(false)  
    })
  }
}
