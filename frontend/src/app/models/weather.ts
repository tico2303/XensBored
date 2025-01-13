export interface WeatherData{
    description:string;
    description_main:string;
    icon_links:string[];
    rain:string|null;
    weather_data:WeatherDetail;
    wind:WindDetail;
}
export interface WeatherDetail{
    feels_like:number;
    grnd_level:number;
    humidity:number;
    sea_level:number;
    temp:number;
    temp_max:number;
    temp_min:number;
}
export interface WindDetail{
    deg:number;
    gust:number;
    speed:number;
}