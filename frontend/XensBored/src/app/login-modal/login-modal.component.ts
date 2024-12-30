import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-login-modal',
  templateUrl: './login-modal.component.html',
  styleUrls: ['./login-modal.component.scss']
})
export class LoginModalComponent {
  username: string = '';
  password: string = '';
  hidePassword: boolean = true;

  constructor(public dialogRef: MatDialogRef<LoginModalComponent>) {}

  close(): void {
    this.dialogRef.close();
  }

  login(): void {
    // Add authentication logic here
    console.log('Logging in with:', this.username, this.password);
    this.dialogRef.close({ username: this.username, password: this.password });
  }
}
