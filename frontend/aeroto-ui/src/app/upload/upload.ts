import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './upload.html',
  styleUrl: './upload.css',

  host: { ngSkipHydration: 'true' }
})
export class Upload {

  selectedResume!: File;
  jdText: string = "";
  score: any;

  constructor(private http: HttpClient) {}

  onResumeSelected(event: any){
    this.selectedResume = event.target.files[0];
  }

upload(){

const formData = new FormData();

formData.append("resume", this.selectedResume);
formData.append("jd", this.jdText);

this.http.post<any>(
"http://localhost:8000/match",
formData
).subscribe(res=>{

console.log(res);   // debug
this.score = res.matchScore;

});

}

}