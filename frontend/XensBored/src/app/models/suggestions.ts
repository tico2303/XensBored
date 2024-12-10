
export interface Suggestion{
    remark:string;
    suggestions:string[];
}
export class SuggestionResults implements Suggestion{
    remark = "" 
    suggestions = [];
}