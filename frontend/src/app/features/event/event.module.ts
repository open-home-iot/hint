import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

// COMPONENTS
import { EventIconsComponent } from './event-icons/event-icons.component';


// SERVICES
import { EventService } from './event.service';

// MODULES
import { EventRoutingModule } from './event-routing.module';


@NgModule({
  declarations: [
    EventIconsComponent
  ],
  imports: [
    EventRoutingModule,
    CommonModule,
    FormsModule
  ],
  exports: [
    EventIconsComponent,
  ],
  providers: [EventService]
})
export class EventModule {}
