import {useEffect, useState} from "react";

const useCountdown = (targetDate: Date, sourceDate?: Date) => {
    const countDownDate = new Date(targetDate).getTime();
    sourceDate = sourceDate === undefined ? new Date() : sourceDate

    const [timeLeft, setTimeLeft] = useState(
        countDownDate - sourceDate.getTime()
    );

    useEffect(() => {
        const interval = setInterval(() => {
            setTimeLeft(countDownDate - new Date().getTime());
        }, 1000);
        return () => clearInterval(interval);
    }, [countDownDate]);

    return composeResult(timeLeft);
};

const composeResult = (timeLeft: number) => {
    const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
    const hours = Math.floor(
        (timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

    return {days, hours, minutes, seconds};
};

export {useCountdown};
