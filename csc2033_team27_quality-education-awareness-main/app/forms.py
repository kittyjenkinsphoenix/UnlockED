import bleach
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, RadioField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

# whitelist for HTML sanitisation
ALLOWED_TAGS = ["b", "i", "u", "em", "strong", "a", "p", "ul", "ol", "li", "br"]
ALLOWED_ATTRIBUTES = {"a": ["href", "title"]}


class LoginForm(FlaskForm):
    username = StringField(
        "Email", validators=[DataRequired(), Email(message="Please enter a valid email address")]
    )  # email validation
    password = PasswordField("Password", validators=[DataRequired()])  # password is required
    submit = SubmitField("Login")


class PasswordResetRequestForm(FlaskForm):
    """Request a password reset link for an account."""

    email = StringField(
        "Email",
        validators=[DataRequired(message="Please enter an email"), Email(message="Please enter a valid email address")],
    )
    submit = SubmitField("Send Reset Link")


class PasswordResetForm(FlaskForm):
    """Set a new password using a reset token."""

    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=10, message="Password must be at least 10 characters long."),
            Regexp(
                r"^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$",
                message="Must include at least one uppercase letter, one digit, and one special character",
            ),
        ],
    )
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Email", validators=[DataRequired(), Email(), Length(max=120)]
    )  # email required, must be valid, no longer than 120

    name = StringField("First Name", validators=[DataRequired()])

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=10, message="Password must be at least 10 characters long."),
            Regexp(
                r"^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$",
                message="Must include at least one uppercase letter, one digit, and one special character",
            ),
        ],
    )

    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match")]
    )

    bio = TextAreaField(
        "Biography", validators=[Length(max=500, message="Bio must be less than 500 characters")]
    )  # sanitised bio

    submit = SubmitField("Register")

    def validate_bio(self, field):
        clean_text = bleach.clean(
            field.data or "", tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True
        )  # remove all unapproved HTML
        field.data = clean_text  # old bio to new sanitised vio


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])

    new_password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=10, message="Password must be at least 10 characters long."),
            Regexp(
                r"^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$",
                message="Must include at least one uppercase letter, one digit, and one special character",
            ),
        ],
    )

    confirm_new_password = PasswordField(
        "Confirm New Password", validators=[DataRequired(), EqualTo("new_password")]
    )  # password must match new password

    submit = SubmitField("Change Password")


class QuizForm(FlaskForm):

    # info for all questions to be used in template
    q1 = RadioField(
        "What is the global literacy rate?",
        choices=[("73.6%", "73.6%"), ("67.3%", "67.3%"), ("86.3%", "86.3%"), ("78.3%", "78.3%")],
        validators=[DataRequired()],
    )

    q2 = RadioField(
        "Which country has the highest USN education score?",
        choices=[
            ("United Kingdom", "United Kingdom"),
            ("Denmark", "Denmark"),
            ("Sweden", "Sweden"),
            ("Finland", "Finland"),
        ],
        validators=[DataRequired()],
    )

    q3 = RadioField(
        "Which country ranked first place in the World Top 20 education rank?",
        choices=[("Finland", "Finland"), ("Japan", "Japan"), ("Denmark", "Denmark"), ("South Korea", "South Korea")],
        validators=[DataRequired()],
    )

    q4 = RadioField(
        "How many children worldwide were out of school in 2023?",
        choices=[
            ("156 million", "156 million"),
            ("272 million", "272 million"),
            ("631 million", "631 million"),
            ("1.12 billion", "1.12 billion"),
        ],
        validators=[DataRequired()],
    )

    q5 = RadioField(
        "How many adults were illiterate in 2024?",
        choices=[
            ("1.43 billion", "1.43 billion"),
            ("943 million", "943 million"),
            ("754 million", "754 million"),
            ("543 million", "543 million"),
        ],
        validators=[DataRequired()],
    )

    q6 = RadioField(
        "What percentage of the world has access to the internet?",
        choices=[("91%", "91%"), ("86%", "86%"), ("74%", "74%"), ("65%", "65%")],
        validators=[DataRequired()],
    )

    submit = SubmitField("Submit")


# form used by take action page for subscribing to emails
class TakeActionForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[DataRequired(message="Please enter an email"), Email(message="Please enter a valid email address")],
    )

    check = BooleanField("take action", validators=[DataRequired(message="Please tick the box to agree")])

    submit = SubmitField("Submit")
