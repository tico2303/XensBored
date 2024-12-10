import { Component, EventEmitter, inject, Output } from '@angular/core';
import { AppService } from '../app.service';
import { MatChipEditedEvent, MatChipInputEvent } from '@angular/material/chips';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import {COMMA, ENTER} from '@angular/cdk/keycodes';
import { Preference } from '../models/perference';
import { switchMap } from 'rxjs';
import { ToastrService } from 'ngx-toastr';
import { SurveyData } from '../models/surveyData';
import { WeatherData } from '../models/weather';

@Component({
  selector: 'app-left-bar',
  templateUrl: './left-bar.component.html',
  styleUrl: './left-bar.component.scss'
})
export class LeftBarComponent {
  public idkOption = 'idk'
  public options = ['indoor', 'outdoor', this.idkOption]
  public interests = ['xbox'];
 // public selectedCategory =''
  //public energyLevel = 1;
  //public zipCode =''
  public surveyData:SurveyData ={
    interests:[],
    selectedCategory:'',
    energyLevel:5,
    zipCode:null,
  }
  weather:WeatherData = Object.create(null);
  addOnBlur = true;
  readonly separatorKeysCodes = [ENTER, COMMA] as const;
  announcer = inject(LiveAnnouncer);
  maxChips = 10
  constructor(private appService:AppService, private toastr:ToastrService){}
  ngOnInit() {
    this.interests = []
  }

  add(event:MatChipInputEvent){
    const value = (event.value || '').trim();
    if (value) {
      if(this.surveyData.interests.length >= this.maxChips){
        this.toastr.warning("Only 10 things allowed bro!")
      }else{
        this.surveyData.interests.push(value);

      }
    }
    // Clear the input value
    event.chipInput!.clear();
  }
  remove(interest: string): void {
    const index = this.surveyData.interests.indexOf(interest);

    if (index >= 0) {
      this.surveyData.interests.splice(index, 1);

      this.announcer.announce(`Removed ${interest}`);
    }
  }

  edit(interest: string, event: MatChipEditedEvent) {
    const value = event.value.trim();

    // Remove fruit if it no longer has a name
    if (!value) {
      this.remove(interest);
      return;
    }

    // Edit existing fruit
    const index = this.surveyData.interests.indexOf(interest);
    if (index >= 0) {
      this.surveyData.interests[index] = value;
    }
  }
  updateEnergyLevel(event:any){
    console.log("updaging energy level")
    console.log(JSON.stringify(event))
    this.surveyData.energyLevel =event.value; 
  }
  formatEngeryLabel(value:number):string{
    if(value==11){
      return 'Cooking'
    }
    if(value == 1){
      return 'Cooked'
    }
    return `${value}`
  }
  onZipChange(event:any){
    if(event.length === 5){
      //make api call to get weather data
      console.log("zip: ", this.surveyData.zipCode)
      this.appService.getWeatherData(this.surveyData.zipCode).subscribe((data)=>{
        console.log(JSON.stringify(data))
        this.weather = data;
      })
    }
  }
  submit(){
    console.log("submitting interests and category")
    if (this.surveyData.selectedCategory === this.idkOption){
      this.surveyData.selectedCategory = 'indoor and outdoor'
    }
    console.log(this.surveyData.interests)
    console.log(this.surveyData.selectedCategory)
    this.appService.loading.next(true);
    const payload:Preference = {
      category:this.surveyData.selectedCategory,
      items:this.surveyData.interests,
      zipCode:this.surveyData.zipCode,
      energyLevel:this.surveyData.energyLevel
    }
    this.appService.addPreference(payload)
    .subscribe((response)=>{
      this.appService.fetchSuggestions()
    })
  }

}
