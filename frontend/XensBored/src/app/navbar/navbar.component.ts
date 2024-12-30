import { Component } from '@angular/core';
import { LoginModalComponent } from '../login-modal/login-modal.component';
import { MatDialog } from '@angular/material/dialog';
@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent {

  constructor( private dialog:MatDialog){}
  openLoginModal(){
    const dialogRef = this.dialog.open(LoginModalComponent, {
      width: '450px',
      position: { 
        top: '10%',
        left:'30%'
      },
      panelClass:'dark-mode-dialog',
      disableClose: true
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        console.log('Login data:', result);
      } else {
        console.log('Login modal closed without action.');
      }
    });
  }
}
