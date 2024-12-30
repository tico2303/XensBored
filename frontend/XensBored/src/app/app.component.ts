
import { Component } from '@angular/core';
import { Preference } from './models/perference';
import { AppService } from './app.service';
import { Suggestion, SuggestionResults } from './models/suggestions';
import { MatDialog } from '@angular/material/dialog';
import { LoginModalComponent } from './login-modal/login-modal.component';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'XensBored';
  suggestion:Suggestion = new SuggestionResults();

  constructor(private appService:AppService, private dialog:MatDialog){}
  sidenavOpened:boolean = true;
  handlePreferencesChange(event:Preference){
    console.log("handlePreferencesChange...")
    /*
    this.appService.addPreference(event.category, event.items)
    this.appService.getSuggestions().subscribe((results:Suggestion)=>{
      this.suggestion = results
    })
      */
  }   
}
