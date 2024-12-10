import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { Suggestion } from './models/suggestions';
import { Preference } from './models/perference';
import { WeatherData } from './models/weather';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  private suggestionData = new BehaviorSubject<Suggestion>({remark:'',suggestions:[]});
  currentSuggestion = this.suggestionData.asObservable();
  public loading = new BehaviorSubject<boolean>(true);
  isLoading = this.loading.asObservable();
  constructor(private http: HttpClient) { }
  fetchSuggestions(){
    console.log("Fetching Suggestions")
    const url = '/suggest'
    this.http.get<Suggestion>(url).subscribe((data)=>{
      this.suggestionData.next(data);
      this.loading.next(false)
    });
  }
  addPreference(preference:Preference){
    const url = '/preference';
    return this.http.post(url, preference);
  }
  clearPreferences(){
    const url = '/preference';
    return this.http.delete(url).subscribe();
  }
  getWeatherData(zipCode:number|null):Observable<WeatherData>{
    const url ='/weather/' + zipCode;
    console.log("url: ", url)
    return this.http.get<WeatherData>(url)
  }

}

    /*
   return of(
    {
      "remark": "Ayo, you tryna beat the boredom? Let\u2019s get it poppin\u2019 with some indoor vibes! No cap, these activities are straight fire! \ud83d\udd25",
      "suggestions": [
          "Host a TikTok dance-off and flex your rizz, but make sure to skibbidy your way to the top!",
          "Create a meme wall and see who can come up with the most sus memes \u2013 winner gets the phantom tax of snacks!",
          "Try your hand at some DIY drip \u2013 customize your clothes and make \u2018em look like a whole mood!",
          "Binge-watch a series and rate the characters on their alpha or sigma energy \u2013 who\u2019s the real MVP?",
          "Start a cooking challenge and see who can make the most slay dish without burning the house down!",
          "Set up a mini indoor Olympics with random household items \u2013 who can throw a pillow the farthest?",
          "Write a short skit with your friends and perform it like you\u2019re on Broadway, but make it extra cringy for the laughs!"
      ]
  })
    */