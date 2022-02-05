from typing import Callable, Optional, TypeVar, Union

from rx import operators as ops
from rx.core import ConnectableObservable, Observable, abc, typing
from rx.core.typing import Mapper
from rx.subject import ReplaySubject

_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")


def replay_(
    mapper: Optional[Mapper[_T1, _T2]] = None,
    buffer_size: Optional[int] = None,
    window: Optional[typing.RelativeTime] = None,
    scheduler: Optional[abc.SchedulerBase] = None,
) -> Callable[[Observable[_T1]], Union[Observable[_T2], ConnectableObservable[_T2]]]:
    """Returns an observable sequence that is the result of invoking the
    mapper on a connectable observable sequence that shares a single
    subscription to the underlying sequence replaying notifications
    subject to a maximum time length for the replay buffer.

    This operator is a specialization of Multicast using a
    ReplaySubject.

    Examples:
        >>> res = replay(buffer_size=3)
        >>> res = replay(buffer_size=3, window=500)
        >>> res = replay(None, 3, 500)
        >>> res = replay(lambda x: x.take(6).repeat(), 3, 500)

    Args:
        mapper: [Optional] Selector function which can use the multicasted
            source sequence as many times as needed, without causing
            multiple subscriptions to the source sequence. Subscribers to
            the given source will receive all the notifications of the
            source subject to the specified replay buffer trimming policy.
        buffer_size: [Optional] Maximum element count of the replay
            buffer.
        window: [Optional] Maximum time length of the replay buffer.
        scheduler: [Optional] Scheduler the observers are invoked on.

    Returns:
        An observable sequence that contains the elements of a
    sequence produced by multicasting the source sequence within a
    mapper function.
    """

    if mapper:

        def subject_factory(scheduler: abc.SchedulerBase) -> ReplaySubject[_T2]:
            return ReplaySubject(buffer_size, window, scheduler)

        return ops.multicast(subject_factory=subject_factory, mapper=mapper)

    return ops.multicast(ReplaySubject(buffer_size, window, scheduler))


__all__ = ["replay_"]
