import { ValidatorFn, FormGroup, ValidationErrors } from '@angular/forms';

export const PASSWORD_VALIDATOR: ValidatorFn = (control: FormGroup): ValidationErrors | null => {
  const PASSWORD = control.get('auth.password');
  const CONFIRM_PASSWORD = control.get('auth.confirmPassword');
  return PASSWORD.value !== CONFIRM_PASSWORD.value ? { noMatch: true } : null;
};
