# Counsellor Database Summary

## ✅ Successfully Created 10 Dummy Counsellors

### Database Records Created:
- **10 CustomUser records** with `user_type='Counsellor'` and `email_verified=True`
- **10 Psychologist records** linked to CustomUser via `Auth_id`
- **10 AdditionalPsycDetails records** linked to Psychologist

### Counsellor Details:

| Username | Name | RCI Number | Experience | Email |
|----------|------|------------|------------|-------|
| dr_smith | Dr. Sarah Smith | RCI123456 | 8 years | dr.smith@euphoria.com |
| dr_johnson | Dr. Michael Johnson | RCI123457 | 12 years | dr.johnson@euphoria.com |
| dr_williams | Dr. Emily Williams | RCI123458 | 6 years | dr.williams@euphoria.com |
| dr_brown | Dr. David Brown | RCI123459 | 15 years | dr.brown@euphoria.com |
| dr_davis | Dr. Jessica Davis | RCI123460 | 9 years | dr.davis@euphoria.com |
| dr_miller | Dr. Christopher Miller | RCI123461 | 11 years | dr.miller@euphoria.com |
| dr_wilson | Dr. Amanda Wilson | RCI123462 | 7 years | dr.wilson@euphoria.com |
| dr_moore | Dr. Robert Moore | RCI123463 | 13 years | dr.moore@euphoria.com |
| dr_taylor | Dr. Lisa Taylor | RCI123464 | 5 years | dr.taylor@euphoria.com |
| dr_anderson | Dr. James Anderson | RCI123465 | 10 years | dr.anderson@euphoria.com |

### Login Credentials:
- **Default Password**: `counsellor123` (for all counsellors)
- **User Type**: Counsellor
- **Email Verified**: True

### Features Now Available:
1. ✅ Appointment booking with counsellor selection
2. ✅ Counsellor dashboard access
3. ✅ Pending approval system
4. ✅ Daily log functionality
5. ✅ Email verification system working

### Next Steps:
- Test appointment booking at: `http://127.0.0.1:8000/appointment/`
- Test counsellor login with any of the created accounts
- Verify that counsellors appear in the appointment form dropdown
