(deftemplate applicant
   (slot name)
   (slot age)
   (slot employment)
   (slot income)
   (slot credit)
   (slot loan-amount)
)

(deftemplate decision
   (slot result)
   (slot reason)
   (slot approved-amount)
)

(defrule decline-underage
   (declare (salience 100))
   (applicant
      (age ?age&:(< ?age 18))
   )
   (not (decision))
   =>
   (assert
      (decision
         (result DECLINED)
         (reason "Applicant is under 18.")
         (approved-amount 0)
      )
   )
)

(defrule decline-no-job
   (declare (salience 90))
   (applicant
      (employment no)
   )
   (not (decision))
   =>
   (assert
      (decision
         (result DECLINED)
         (reason "Applicant has no job.")
         (approved-amount 0)
      )
   )
)

(defrule decline-poor-credit
   (declare (salience 80))
   (applicant
      (credit poor)
   )
   (not (decision))
   =>
   (assert
      (decision
         (result DECLINED)
         (reason "Applicant has poor credit.")
         (approved-amount 0)
      )
   )
)

(defrule conditional-low-income
   (declare (salience 70))
   (applicant
      (employment yes)
      (income ?income&:(and (>= ?income 1000)
                            (<= ?income 5000)))
      (credit average)
      (loan-amount ?requested)
   )
   (not (decision))
   =>
   (bind ?amount (/ ?requested 2))

   (if (> ?amount 10000)
      then
      (bind ?amount 10000)
   )

   (assert
      (decision
         (result CONDITIONAL)
         (reason "Applicant has a job, low income, and average credit.")
         (approved-amount ?amount)
      )
   )
)

(defrule conditional-mid-income
   (declare (salience 70))
   (applicant
      (employment yes)
      (income ?income&:(and (>= ?income 6000)
                            (<= ?income 15000)))
      (credit average)
      (loan-amount ?requested)
   )
   (not (decision))
   =>
   (bind ?amount (/ ?requested 2))

   (if (> ?amount 10000)
      then
      (bind ?amount 10000)
   )

   (assert
      (decision
         (result CONDITIONAL)
         (reason "Applicant has a job, mid income, and average credit.")
         (approved-amount ?amount)
      )
   )
)

(defrule approved-mid-income
   (declare (salience 60))
   (applicant
      (employment yes)
      (income ?income&:(and (>= ?income 6000)
                            (<= ?income 15000)))
      (credit good)
      (loan-amount ?requested)
   )
   (not (decision))
   =>
   (assert
      (decision
         (result APPROVED)
         (reason "Applicant has a job, mid income, and good credit.")
         (approved-amount ?requested)
      )
   )
)

(defrule approved-high-average
   (declare (salience 60))
   (applicant
      (employment yes)
      (income ?income&:(>= ?income 16000))
      (credit average)
      (loan-amount ?requested)
   )
   (not (decision))
   =>
   (assert
      (decision
         (result APPROVED)
         (reason "Applicant has a job, high income, and average credit.")
         (approved-amount ?requested)
      )
   )
)

(defrule approved-high-good
   (declare (salience 60))
   (applicant
      (employment yes)
      (income ?income&:(>= ?income 16000))
      (credit good)
      (loan-amount ?requested)
   )
   (not (decision))
   =>
   (assert
      (decision
         (result APPROVED)
         (reason "Applicant has a job, high income, and good credit.")
         (approved-amount ?requested)
      )
   )
)

(defrule display-result
   (decision
      (result ?result)
      (reason ?reason)
      (approved-amount ?amount)
   )
   =>
   (printout t crlf
      "=========================" crlf
      "Please fill all the following....." crlf
      "Result: " ?result crlf
      "Reason: " ?reason crlf
      "Approved Amount: PHP " ?amount crlf
      "=========================" crlf
   )
)