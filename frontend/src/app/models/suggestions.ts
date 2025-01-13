
export interface Suggestion{
    remark:string;
    suggestions:string[];
    status?:string;
    message?:string;
}
export class SuggestionResults implements Suggestion{
    remark = "" 
    suggestions = [];
}