import { Component, signal } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { Upload } from './upload/upload';

@Component({
  selector: 'app-root',
  imports: [HttpClientModule, Upload],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('aeroto-ui');
}