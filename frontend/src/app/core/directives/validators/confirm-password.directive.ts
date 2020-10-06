import { ValidatorFn, FormGroup, ValidationErrors } from '@angular/forms';

export const passwordValidator: ValidatorFn = (control: FormGroup): ValidationErrors | null => {
  const password = control.get('auth.password');
  const confirmPassword = control.get('auth.confirmPassword');
  return password.value !== confirmPassword.value ? { noMatch: true } : null;
}
